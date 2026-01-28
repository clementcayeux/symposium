

from django.shortcuts import render

# Cette fonction correspond à views.home
def home(request):
    return render(request, 'core/index.html')




from .models import Membre, ConfigurationSite

def equipe(request):
    membres = Membre.objects.all()
    # On récupère la première (et seule) ligne de config, ou None
    config = ConfigurationSite.objects.first()
    
    return render(request, 'core/equipe.html', {
        'membres': membres,
        'config': config 
    })


# Cette fonction correspond à views.mentions_legales
def mentions_legales(request):
    return render(request, 'core/mentions_legales.html')


from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import ContactRecipient


def contact(request):
    if request.method == 'POST':
        # 1. On vérifie le piège (Honeypot)
        honeypot = request.POST.get('phone_confirm')
        if honeypot:
            # C'est un robot ! On ne fait rien, on ne dépense pas de crédit mail.
            # On simule un succès pour que le robot ne cherche pas d'autre faille.
            messages.success(request, "Votre message a été envoyé. Un mail de confirmation vous a été adressé.")
            return redirect('contact')

        # 2. Si le champ est vide, c'est un humain, on continue la logique normale
        nom = request.POST.get('name')
        email_utilisateur = request.POST.get('email')
        sujet = request.POST.get('subject')
        message_contenu = request.POST.get('message')

        # --- RÉCUPÉRATION DYNAMIQUE DES DESTINATAIRES ---
        # On récupère tous les emails actifs dans une liste
        destinataires = list(ContactRecipient.objects.filter(actif=True).values_list('email', flat=True))
        
        # Sécurité : Si aucun mail n'est configuré dans l'admin, on met un mail par défaut 
        # pour éviter que send_mail ne plante
        if not destinataires:
            destinataires = ['clement.cayeux@symposium-cs.fr']

        # --- 1. MAIL POUR LES MEMBRES SYMPO (L'alerte admin) ---
        corps_admin = f"Nouveau message par le formulaire du site, de : {nom} ({email_utilisateur})\n\nSujet : {sujet}\n\nContenu :\n{message_contenu}"
        
        # --- 2. MAIL POUR L'UTILISATEUR (La confirmation) ---
        # corps_confirmation = f"Bonjour {nom},\n\nNous avons bien reçu votre message concernant : '{sujet}'.\n\nL'équipe de Symposium CentraleSupélec va l'étudier avec attention et reviendra vers vous dès que possible.\n\nCordialement,\n\nL'équipe Symposium, \n\n Ceci est un message automatique, merci de ne pas répondre."
        context = {'nom': nom, 'sujet': sujet}
        html_message = render_to_string('core/emails/confirmation_email.html', context)
        plain_message = strip_tags(html_message) # Version texte brut pour les vieux téléphones

        try:
            # Envoi à l'administrateur $$$
            send_mail(
                subject=f"[Contact WEB] {sujet}",
                message=corps_admin,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=destinataires, # Utilise la liste de la BDD
                fail_silently=False,
            )


            # Envoi de la confirmation HTML à l'utilisateur
            send_mail(
                "Confirmation de réception - Symposium CentraleSupélec",
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [email_utilisateur],
                html_message=html_message, # C'est ici qu'on active le HTML
            )


            messages.success(request, "Votre message a été envoyé. Un mail de confirmation vous a été adressé (Veuillez vérifier vos spams).")
            return redirect('contact')

        except Exception as e:
            messages.error(request, f"Une erreur est survenue : {e}")

    return render(request, 'core/contact.html')



from .models import Evenement

def home(request):
    # On récupère les 3 prochaines conférences non passées
    prochains_evenements = Evenement.objects.filter(est_passee=False).order_by('date_evenement')[:3]
    # On récupère les replays (si tu crées aussi un modèle pour eux)
    
    return render(request, 'core/index.html', {'evenements': prochains_evenements})




from django.utils import timezone
from django.db.models import Q

def home(request):
    # On récupère l'heure actuelle
    maintenant = timezone.now()
    
    # On veut les événements qui ne sont pas encore terminés
    evenements = Evenement.objects.filter(
    Q(date_debut__gte=maintenant) | Q(date_fin__gte=maintenant),
    est_publie=True
).distinct().order_by('date_debut')

    return render(request, 'core/index.html', {'evenements': evenements})






