from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.db.models import Q
from django.core.mail import EmailMessage
import time
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django_ratelimit.decorators import ratelimit

from .models import Evenement, Partenaire, Membre, ConfigurationSite, ContactRecipient, Replay

# --- PAGE D'ACCUEIL (Fusion de home et index) ---
def index(request):
    """Affiche les prochains événements et les partenaires sur la home"""
    maintenant = timezone.now()
    
    # 1. On récupère les événements à venir ou en cours (publiés)
    # On affiche les 3 plus proches
    prochains_evenements = Evenement.objects.filter(
        Q(date_debut__gte=maintenant) | Q(date_fin__gte=maintenant),
        est_publie=True
    ).distinct().order_by('date_debut')[:3]

    # 2. On récupère tous les partenaires (ordonnés par le champ ordre)
    partenaires = Partenaire.objects.all().order_by('ordre')

    # ON RÉCUPÈRE LES 3 PREMIERS REPLAYS
    replays = Replay.objects.all()[:3]
    
    return render(request, 'core/index.html', {
        'evenements': prochains_evenements,
        'partenaires': partenaires,
        'replays': replays
    })


# --- PAGE ÉQUIPE ---
def equipe(request):
    """Affiche les membres de l'asso et l'année de promo dynamique"""
    membres = Membre.objects.all().order_by('ordre')
    config = ConfigurationSite.objects.first()
    
    return render(request, 'core/equipe.html', {
        'membres': membres,
        'config': config 
    })


# --- PAGE CONTACT (Avec gestion Email & Honeypot) ---
@ratelimit(key='ip', rate='4/m', method='POST', block=False)
def contact(request):
    # Vérifier si la limite a été atteinte
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        messages.error(request, "Trop de tentatives. Veuillez attendre une minute.")
        return redirect('contact')

    if request.method == 'POST':
        # 1. Honeypot pour bloquer les robots
        honeypot = request.POST.get('website')
        if honeypot:
            messages.success(request, "Message envoyé.")
            return redirect('contact')
        
        timestamp = request.POST.get('form_timestamp')
        if timestamp:
            time_elapsed = time.time() - float(timestamp)
            if time_elapsed < 4:  # Moins de 4 secondes = Bot
                return redirect('contact')        

        # 2. Récupération des données du formulaire
        nom = request.POST.get('name')
        email_utilisateur = request.POST.get('email')
        sujet = request.POST.get('subject')
        message_contenu = request.POST.get('message')

        # 3. Récupération des destinataires actifs en BDD
        destinataires = list(ContactRecipient.objects.filter(actif=True).values_list('email', flat=True))
        if not destinataires:
            destinataires = ['contact@symposium-cs.fr']

        # Nettoyage basique
        nom = nom.strip() if nom else ""
        email_utilisateur = email_utilisateur.strip().lower() if email_utilisateur else ""
        sujet = sujet.strip() if sujet else ""
        message_contenu = message_contenu.strip() if message_contenu else ""

        # Validation nom
        if not nom or len(nom) < 2 or len(nom) > 100:
            messages.error(request, "Merci d’indiquer un nom valide.")
            return redirect('contact')

        # Validation email
        try:
            validate_email(email_utilisateur)
        except ValidationError:
            messages.error(request, "Adresse email invalide.")
            return redirect('contact')

        # Validation sujet
        if not sujet or len(sujet) > 200:
            messages.error(request, "Sujet invalide ou trop long.")
            return redirect('contact')

        # Validation message
        if not message_contenu or len(message_contenu) < 10:
            messages.error(request, "Le message doit contenir au moins 10 caractères.")
            return redirect('contact')

        if len(message_contenu) > 20000:
            messages.error(request, "Message trop long.")
            return redirect('contact')

        
        # 4. Préparation du mail pour l'équipe (Admin)
        sujet_admin = f"[FORMULAIRE WEB] {sujet}"
        corps_admin = f"""
Un nouveau message a été reçu via le formulaire du site web.

EXPÉDITEUR : {nom}
EMAIL : {email_utilisateur}
SUJET : {sujet}

(Se coordoner pour répondre une fois, mettre contact@symposium-cs.fr en copie de la réponse pour l'archivage)
-----------------------------------------------------------

MESSAGE :
{message_contenu}

-----------------------------------------------------------

        """

        # Confirmation pour l'utilisateur
        context = {'nom': nom, 'sujet': sujet}
        html_message = render_to_string('core/emails/confirmation_email.html', context)
        plain_message = strip_tags(html_message)

        try:

            
            # Envoi mail admin 
            mail_admin = EmailMessage(
                subject=sujet_admin,
                body=corps_admin,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=destinataires,
            )
            mail_admin.send()

            # Envoi mail confirmation client
            send_mail(
                "Confirmation de réception - Symposium CentraleSupélec",
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [email_utilisateur],
                html_message=html_message,
            )

            messages.success(request, "Merci, votre message a bien été envoyé. Vous avez reçu un mail de confirmation (veuillez vérifier vos spams).")
            return redirect('contact')

        except Exception as e:
            messages.error(request, f"Erreur lors de l'envoi : {e}")

    return render(request, 'core/contact.html')


# --- PAGES STATIQUES ---
def mentions_legales(request):
    return render(request, 'core/mentions_legales.html')