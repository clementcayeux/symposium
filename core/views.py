

from django.shortcuts import render

# Cette fonction correspond à views.home
def home(request):
    return render(request, 'core/index.html')

# Cette fonction correspond à views.equipe
def equipe(request):
    return render(request, 'core/equipe.html')

# Cette fonction correspond à views.mentions_legales
def mentions_legales(request):
    return render(request, 'core/mentions_legales.html')


from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

from django.template.loader import render_to_string
from django.utils.html import strip_tags



def contact(request):
    if request.method == 'POST':
        nom = request.POST.get('name')
        email_utilisateur = request.POST.get('email')
        sujet = request.POST.get('subject')
        message_contenu = request.POST.get('message')

        # --- 1. MAIL POUR CLÉMENT (L'alerte admin) ---
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
                recipient_list=['clement.cayeux@symposium-cs.fr'],
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


            messages.success(request, "Votre message a été envoyé. \n Un mail de confirmation vous a été adressé (Veuillez vérifier vos spams).")
            return redirect('contact')

        except Exception as e:
            messages.error(request, f"Une erreur est survenue : {e}")

    return render(request, 'core/contact.html')

