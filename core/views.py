from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.db.models import Q

from .models import Evenement, Partenaire, Membre, ConfigurationSite, ContactRecipient

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
    
    return render(request, 'core/index.html', {
        'evenements': prochains_evenements,
        'partenaires': partenaires
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
def contact(request):
    if request.method == 'POST':
        # 1. Honeypot pour bloquer les robots
        honeypot = request.POST.get('phone_confirm')
        if honeypot:
            messages.success(request, "Votre message a été envoyé.")
            return redirect('contact')

        # 2. Récupération des données du formulaire
        nom = request.POST.get('name')
        email_utilisateur = request.POST.get('email')
        sujet = request.POST.get('subject')
        message_contenu = request.POST.get('message')

        # 3. Récupération des destinataires actifs en BDD
        destinataires = list(ContactRecipient.objects.filter(actif=True).values_list('email', flat=True))
        if not destinataires:
            destinataires = ['clement.cayeux@symposium-cs.fr']

        # 4. Préparation des emails
        # Alerte pour l'équipe
        corps_admin = f"Nouveau message de : {nom} ({email_utilisateur})\n\nSujet : {sujet}\n\nMessage :\n{message_contenu}"
        
        # Confirmation pour l'utilisateur
        context = {'nom': nom, 'sujet': sujet}
        html_message = render_to_string('core/emails/confirmation_email.html', context)
        plain_message = strip_tags(html_message)

        try:
            # Envoi mail admin
            send_mail(
                subject=f"[Contact WEB] {sujet}",
                message=corps_admin,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=destinataires,
                fail_silently=False,
            )

            # Envoi mail confirmation client
            send_mail(
                "Confirmation de réception - Symposium CentraleSupélec",
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [email_utilisateur],
                html_message=html_message,
            )

            messages.success(request, "Message envoyé ! Vérifiez vos spams pour la confirmation.")
            return redirect('contact')

        except Exception as e:
            messages.error(request, f"Erreur lors de l'envoi : {e}")

    return render(request, 'core/contact.html')


# --- PAGES STATIQUES ---
def mentions_legales(request):
    return render(request, 'core/mentions_legales.html')