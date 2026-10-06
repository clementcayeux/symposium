import json
import time
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.db.models import Q
from django.core.mail import EmailMessage, send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test
from django_ratelimit.decorators import ratelimit
from .models import Invite
from .models import Evenement, Partenaire, Membre, ConfigurationSite, ContactRecipient, Replay
from datetime import datetime
from django.views.decorators.http import require_POST




# --- REDIRECTION DEPUIS /admin/ ---
def admin_entry_redirect(request):
    """Si l'utilisateur est authentifié staff, le renvoie sur le site en mode édition."""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('index')
    return redirect('login')


def custom_logout(request):
    """Déconnecte l'admin et renvoie vers la page d'accueil."""
    auth.logout(request)
    return redirect('index')


# --- PAGE D'ACCUEIL ---
def index(request):
    maintenant = timezone.now()
    
    # Mode édition admin : uniquement si staff ET pas en mode aperçu public (?preview=true)
    is_admin_editing = request.user.is_staff and not request.GET.get('preview')
    
    if is_admin_editing:
        # En mode édition, l'administrateur voit tous les événements (y compris les brouillons)
        prochains_evenements = Evenement.objects.all().order_by('date_debut')[:6]
    else:
        # En mode public (ou preview) : uniquement les événements publiés du jour ou à venir
        prochains_evenements = Evenement.objects.filter(
            Q(date_fin__gte=maintenant) | Q(date_debut__date__gte=maintenant.date()),
            est_publie=True
        ).distinct().order_by('date_debut')[:3]

    partenaires = Partenaire.objects.all().order_by('ordre')
    replays = Replay.objects.all()[:6]
    config, _ = ConfigurationSite.objects.get_or_create(id=1)
    
    return render(request, 'core/index.html', {
        'evenements': prochains_evenements,
        'partenaires': partenaires,
        'replays': replays,
        'config': config,
        'is_admin_editing': is_admin_editing,
    })


# --- PAGE ÉQUIPE ---
def equipe(request):
    membres = Membre.objects.all().order_by('ordre')
    config, _ = ConfigurationSite.objects.get_or_create(id=1)
    is_admin_editing = request.user.is_staff and not request.GET.get('preview')
    
    return render(request, 'core/equipe.html', {
        'membres': membres,
        'config': config,
        'is_admin_editing': is_admin_editing,
    })


# --- PAGE CONTACT ---
@ratelimit(key='ip', rate='4/m', method='POST', block=False)
def contact(request):
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        messages.error(request, "Trop de tentatives. Veuillez attendre une minute.")
        return redirect('contact')

    if request.method == 'POST':
        honeypot = request.POST.get('website')
        if honeypot:
            messages.success(request, "Message envoyé.")
            return redirect('contact')
        
        timestamp = request.POST.get('form_timestamp')
        if timestamp:
            time_elapsed = time.time() - float(timestamp)
            if time_elapsed < 4:
                return redirect('contact')        

        nom = request.POST.get('name', '').strip()
        email_utilisateur = request.POST.get('email', '').strip().lower()
        sujet = request.POST.get('subject', '').strip()
        message_contenu = request.POST.get('message', '').strip()

        destinataires = list(ContactRecipient.objects.filter(actif=True).values_list('email', flat=True))
        if not destinataires:
            destinataires = ['contact@symposium-cs.fr']

        if not nom or len(nom) < 2 or len(nom) > 100:
            messages.error(request, "Merci d’indiquer un nom valide.")
            return redirect('contact')

        try:
            validate_email(email_utilisateur)
        except ValidationError:
            messages.error(request, "Adresse email invalide.")
            return redirect('contact')

        if not sujet or len(sujet) > 200:
            messages.error(request, "Sujet invalide ou trop long.")
            return redirect('contact')

        if not message_contenu or len(message_contenu) < 10 or len(message_contenu) > 20000:
            messages.error(request, "Le message doit contenir entre 10 et 20 000 caractères.")
            return redirect('contact')

        sujet_admin = f"[FORMULAIRE WEB] {sujet}"
        corps_admin = f"""Un nouveau message a été reçu via le formulaire du site web.

EXPÉDITEUR : {nom}
EMAIL : {email_utilisateur}
SUJET : {sujet}

MESSAGE :
{message_contenu}
"""
        context = {'nom': nom, 'sujet': sujet}
        html_message = render_to_string('core/emails/confirmation_email.html', context)
        plain_message = strip_tags(html_message)

        try:
            mail_admin = EmailMessage(
                subject=sujet_admin,
                body=corps_admin,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=destinataires,
            )
            mail_admin.send()

            send_mail(
                "Confirmation de réception - Symposium CentraleSupélec",
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [email_utilisateur],
                html_message=html_message,
            )

            messages.success(request, "Merci, votre message a bien été envoyé. Un email de confirmation vous a été adressé.")
            return redirect('contact')

        except Exception as e:
            messages.error(request, f"Erreur lors de l'envoi : {e}")

    return render(request, 'core/contact.html')


def mentions_legales(request):
    return render(request, 'core/mentions_legales.html')


# ==========================================
# ESPACE RÉGLAGES ADMIN
# ==========================================
@user_passes_test(lambda u: u.is_staff)
def reglages(request):
    config, _ = ConfigurationSite.objects.get_or_create(id=1)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_config':
            annee = request.POST.get('annee_promotion', '').strip()
            if annee and len(annee) == 4 and annee.isdigit():
                config.annee_promotion = annee
                config.save()
                messages.success(request, "Année de promotion mise à jour.")
            else:
                messages.error(request, "L'année doit être au format YYYY (ex: 2026).")

        elif action == 'create_user':
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '')
            is_superuser = request.POST.get('is_superuser') == 'on'

            if not username or not password:
                messages.error(request, "L'identifiant et le mot de passe sont obligatoires.")
            elif User.objects.filter(username=username).exists():
                messages.error(request, "Cet identifiant existe déjà.")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_staff = True
                user.is_superuser = is_superuser
                user.save()
                messages.success(request, f"Compte administrateur '{username}' créé avec succès.")

        elif action == 'change_password':
            user_id = request.POST.get('user_id')
            new_password = request.POST.get('new_password', '')
            user_target = get_object_or_404(User, pk=user_id)
            if new_password and len(new_password) >= 6:
                user_target.set_password(new_password)
                user_target.save()
                messages.success(request, f"Mot de passe mis à jour pour {user_target.username}.")
            else:
                messages.error(request, "Le mot de passe doit comporter au moins 6 caractères.")

        elif action == 'delete_user':
            user_id = request.POST.get('user_id')
            user_target = get_object_or_404(User, pk=user_id)
            if user_target == request.user:
                messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
            else:
                nom = user_target.username
                user_target.delete()
                messages.success(request, f"Le compte '{nom}' a été supprimé.")

        elif action == 'add_recipient':
            nom = request.POST.get('nom', '').strip()
            email = request.POST.get('email', '').strip()
            if nom and email:
                ContactRecipient.objects.create(nom=nom, email=email, actif=True)
                messages.success(request, f"Destinataire {nom} ajouté.")
            else:
                messages.error(request, "Nom et email obligatoires.")

        elif action == 'toggle_recipient':
            rec_id = request.POST.get('recipient_id')
            recipient = get_object_or_404(ContactRecipient, pk=rec_id)
            recipient.actif = not recipient.actif
            recipient.save()
            messages.success(request, f"Statut mis à jour pour {recipient.nom}.")

        elif action == 'delete_recipient':
            rec_id = request.POST.get('recipient_id')
            recipient = get_object_or_404(ContactRecipient, pk=rec_id)
            recipient.delete()
            messages.success(request, "Destinataire supprimé.")

        return redirect('reglages')

    utilisateurs = User.objects.all().order_by('-is_superuser', 'username')
    destinataires = ContactRecipient.objects.all()

    stats = {
        'evenements': Evenement.objects.count(),
        'replays': Replay.objects.count(),
        'partenaires': Partenaire.objects.count(),
        'membres': Membre.objects.count(),
    }

    return render(request, 'core/reglages.html', {
        'config': config,
        'utilisateurs': utilisateurs,
        'destinataires': destinataires,
        'stats': stats,
    })


# ==========================================
# API D'ADMINISTRATION (MODALES & AJAX)
# ==========================================
@require_POST
def api_save_item(request):
    """Gère la création ET la modification d'un élément via FormData"""
    if not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'Non autorisé'}, status=403)

    model_name = request.POST.get('model', '').lower()
    item_id = request.POST.get('id', '')

    try:
        if model_name == 'evenement':
            obj = Evenement.objects.get(pk=item_id) if item_id else Evenement()
            obj.invite = request.POST.get('invite', obj.invite)
            obj.titre = request.POST.get('titre', obj.titre)
            obj.categorie = request.POST.get('categorie', obj.categorie)
            obj.lieu = request.POST.get('lieu', obj.lieu)
            obj.horaires_precision = request.POST.get('horaires_precision', obj.horaires_precision)
            obj.lien_inscription = request.POST.get('lien_inscription', obj.lien_inscription)
            obj.texte_bouton_inscription = request.POST.get('texte_bouton_inscription', "S'inscrire / Billetterie")
            
            # Prise en compte robuste de 'true' ou 'on'
            val_publie = str(request.POST.get('est_publie', '')).strip().lower()
            obj.est_publie = val_publie in ['true', '1', 'on']

            date_debut = request.POST.get('date_debut')
            if date_debut: 
                obj.date_debut = date_debut
            
            date_fin = request.POST.get('date_fin')
            if date_fin: 
                obj.date_fin = date_fin
            elif 'date_fin' in request.POST: 
                obj.date_fin = None

            if 'image' in request.FILES:
                obj.image = request.FILES['image']
            
            obj.save()

        elif model_name == 'replay':
            obj = Replay.objects.get(pk=item_id) if item_id else Replay()
            obj.invite = request.POST.get('invite', obj.invite)
            obj.url_youtube = request.POST.get('url_youtube', obj.url_youtube)
            obj.save()

        elif model_name == 'partenaire':
            obj = Partenaire.objects.get(pk=item_id) if item_id else Partenaire()
            obj.nom = request.POST.get('nom', obj.nom)
            obj.lien = request.POST.get('lien', obj.lien)
            taille = request.POST.get('taille_ajustement')
            if taille and taille.isdigit():
                obj.taille_ajustement = int(taille)
            if 'logo' in request.FILES:
                obj.logo = request.FILES['logo']
            obj.save()

        elif model_name == 'membre':
            obj = Membre.objects.get(pk=item_id) if item_id else Membre()
            obj.nom = request.POST.get('nom', obj.nom)
            obj.role = request.POST.get('role', obj.role)
            ordre = request.POST.get('ordre')
            if ordre and ordre.isdigit():
                obj.ordre = int(ordre)
            if 'photo' in request.FILES:
                obj.photo = request.FILES['photo']
            obj.save()

        elif model_name == 'configurationsite':
            obj = ConfigurationSite.objects.first()
            obj.a_propos_paragraphe_1 = request.POST.get('a_propos_paragraphe_1', obj.a_propos_paragraphe_1)
            obj.a_propos_statement = request.POST.get('a_propos_statement', obj.a_propos_statement)
            obj.a_propos_paragraphe_2 = request.POST.get('a_propos_paragraphe_2', obj.a_propos_paragraphe_2)
            obj.save()

        else:
            return JsonResponse({'status': 'error', 'message': 'Modèle inconnu'}, status=400)

        return JsonResponse({'status': 'success'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@require_POST
def api_delete_item(request):
    """Suppression d'un élément."""
    if not request.user.is_staff:
        return JsonResponse({'status': 'error'}, status=403)

    try:
        data = json.loads(request.body)
        model_name = data.get('model', '').lower()
        item_id = data.get('id')

        if model_name == 'evenement': Evenement.objects.filter(pk=item_id).delete()
        elif model_name == 'replay': Replay.objects.filter(pk=item_id).delete()
        elif model_name == 'partenaire': Partenaire.objects.filter(pk=item_id).delete()
        elif model_name == 'membre': Membre.objects.filter(pk=item_id).delete()
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def liste_invites(request):
    categorie = request.GET.get('cat')
    invites = Invite.objects.all()[:30]
    if categorie:
        invites = invites.filter(categorie=categorie)
    
    return render(request, 'core/invites.html', {
        'invites': invites,
        'categorie_active': categorie,
    })



@require_POST
@user_passes_test(lambda u: u.is_staff)
def api_sauvegarder_invite(request):
    try:
        data = json.loads(request.body)
        invite_id = data.get('id')
        nom = data.get('nom', '').strip()
        fonction = data.get('fonction', '').strip()
        youtube_url = data.get('youtube_url', '').strip()
        categorie = data.get('categorie', 'economie')
        ordre = int(data.get('ordre', 100) or 100)
        
        date_str = data.get('date_venue')
        date_venue = None
        if date_str:
            try:
                date_venue = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        if not nom or not youtube_url:
            return JsonResponse({'success': False, 'error': 'Le nom et le lien YouTube sont requis.'}, status=400)

        if invite_id:
            invite = Invite.objects.get(id=invite_id)
            invite.nom = nom
            invite.fonction = fonction
            invite.youtube_url = youtube_url
            invite.categorie = categorie
            invite.ordre = ordre
            invite.date_venue = date_venue
            invite.save()
        else:
            invite = Invite.objects.create(
                nom=nom,
                fonction=fonction,
                youtube_url=youtube_url,
                categorie=categorie,
                ordre=ordre,
                date_venue=date_venue
            )

        return JsonResponse({'success': True, 'id': invite.id})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_POST
@user_passes_test(lambda u: u.is_staff)
def api_supprimer_invite(request):
    try:
        data = json.loads(request.body)
        invite_id = data.get('id')
        if not invite_id:
            return JsonResponse({'success': False, 'error': 'ID manquant.'}, status=400)
        
        Invite.objects.filter(id=invite_id).delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

