

from django.shortcuts import render

# Cette fonction correspond à views.home
def home(request):
    return render(request, 'core/index.html')

# Cette fonction correspond à views.equipe
def equipe(request):
    return render(request, 'core/equipe.html')


from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Construction du mail
        full_message = f"Message de {name} ({email}) :\n\n{message}"
        
        try:
            send_mail(
                f"[Contact Symposium] {subject}",
                full_message,
                email, # Expéditeur
                ['clement.cayeux@symposium-cs.fr'], # Destinataire
                fail_silently=False,
            )
            messages.success(request, "Votre message a bien été envoyé !")
            return redirect('contact')
        except Exception:
            messages.error(request, "Une erreur est survenue lors de l'envoi.")

    return render(request, 'core/contact.html')