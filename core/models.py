import os
import re
from io import BytesIO
from PIL import Image, ImageOps

from django.db import models
from django.utils import timezone
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver


# =====================================================================
# UTILITAIRE DE COMPRESSION & OPTIMISATION D'IMAGES (WEBP)
# =====================================================================
def optimize_image_field(image_field, max_dim=1600, quality=80):
    """
    Redimensionne et convertit en WebP toute image nouvellement téléversée.
    Préserve le canal alpha (transparence) pour les logos.
    """
    if not image_field or not hasattr(image_field, 'file'):
        return

    # On ne compresse que les fichiers nouvellement téléversés (pas les fichiers déjà en base)
    if not isinstance(image_field.file, UploadedFile):
        return

    try:
        img = Image.open(image_field.file)
        img = ImageOps.exif_transpose(img)  # Corrige l'orientation des photos smartphone

        # Redimensionnement proportionnel si l'image dépasse la taille maximale
        if img.width > max_dim or img.height > max_dim:
            img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)

        output = BytesIO()
        filename, _ = os.path.splitext(os.path.basename(image_field.name))

        # Enregistrement en WebP (supporte la transparence et compresse fortement)
        img.save(output, format='WEBP', quality=quality, method=6)
        output.seek(0)

        new_filename = f"{filename}.webp"
        image_field.save(new_filename, ContentFile(output.read()), save=False)
    except Exception:
        # En cas de format inhabituel, on ne bloque pas l'enregistrement
        pass


# =====================================================================
# MODÈLES
# =====================================================================
class Evenement(models.Model):
    TYPE_CHOICES = [
        ('CONF', 'Conférence'),
        ('TABLE', 'Table Ronde'),
        ('WORK', 'Atelier / Workshop'),
        ('HACK', 'Hackathon'),
        ('TRIP', "Voyage d'étude"),
        ('AUTRE', 'Autre'),
    ]

    invite = models.CharField(max_length=200, help_text="Nom de l'intervenant ou nom du projet")
    titre = models.CharField(max_length=400, help_text="Description")
    categorie = models.CharField(max_length=100, default="Politique", help_text="Le petit texte couleur or")
    type_evenement = models.CharField(max_length=10, choices=TYPE_CHOICES, default='CONF')

    date_debut = models.DateTimeField(verbose_name="Date et heure de début")
    date_fin = models.DateTimeField(null=True, blank=True, verbose_name="Date et heure de fin (optionnel)")
    horaires_precision = models.CharField(max_length=100, blank=True, help_text="Ex: 'Toute la journée' ou '14h-18h'")

    lieu = models.CharField(max_length=200, default="Amphi Michelin")
    image = models.ImageField(upload_to='evenements/')
    lien_inscription = models.URLField(blank=True, null=True, help_text="Lien vers la billetterie ou l'événement")
    texte_bouton_inscription = models.CharField(max_length=50, default="S'inscrire / Billetterie", blank=True)
    
    est_publie = models.BooleanField(default=True, help_text="Décocher pour passer en brouillon")

    class Meta:
        verbose_name = "Événement"
        ordering = ['-date_debut']

    def __str__(self):
        return f"{self.invite} - {self.titre}"

    def save(self, *args, **kwargs):
        optimize_image_field(self.image, max_dim=1600, quality=82)
        super().save(*args, **kwargs)

    @property
    def est_passe(self):
        date_reference = self.date_fin if self.date_fin else self.date_debut
        if not date_reference:
            return False
        return date_reference < timezone.now()


class ContactRecipient(models.Model):
    nom = models.CharField(max_length=100, help_text="Nom du membre")
    email = models.EmailField()
    actif = models.BooleanField(default=True, help_text="Décocher pour ne plus recevoir les mails temporairement")

    def __str__(self):
        return f"{self.nom} ({self.email})"

    class Meta:
        verbose_name = "Destinataire des messages du formulaire"
        verbose_name_plural = "Destinataires des messages du formulaire"


class Membre(models.Model):
    nom = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='equipe/')
    ordre = models.PositiveIntegerField(default=100, help_text="Plus petit nombre = apparaît en premier")

    class Meta:
        verbose_name = "Membre de l'équipe"
        ordering = ['ordre', 'nom']

    def __str__(self):
        return f"{self.nom} ({self.role})"

    def save(self, *args, **kwargs):
        optimize_image_field(self.photo, max_dim=1000, quality=82)
        super().save(*args, **kwargs)


class ConfigurationSite(models.Model):
    annee_promotion = models.CharField(max_length=4, default="2026", help_text="L'année affichée pour l'équipe (ex: 2026)")
    a_propos_paragraphe_1 = models.TextField(
        default="Fondée en 2014, Symposium est la tribune étudiante de CentraleSupélec. Chaque mois, nous invitons des personnalités du monde politique, économique, culturel et académique à participer à des conférences et débats, afin d’échanger sans filtre avec les étudiants.",
        blank=True
    )
    a_propos_statement = models.TextField(
        default="À l’heure où les enjeux contemporains deviennent toujours plus techniques, Symposium défend la conviction que les ingénieurs et scientifiques doivent être pleinement acteurs du débat démocratique.",
        blank=True
    )
    a_propos_paragraphe_2 = models.TextField(
        default="Symposium s’adresse en premier lieu aux étudiants de CentraleSupélec, auxquels s’ajoutent régulièrement ceux de l’ENS Paris-Saclay, de l’École Polytechnique et, plus largement, des établissements du Plateau de Saclay.",
        blank=True
    )

    class Meta:
        verbose_name = "Configuration du site"
        verbose_name_plural = "Configuration du site"

    def __str__(self):
        return "Paramètres généraux"


class Partenaire(models.Model):
    nom = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='partenaires/')
    lien = models.URLField(blank=True, help_text="Lien vers leur site web")
    ordre = models.PositiveIntegerField(default=100, help_text="Petit nombre = apparaît en premier")
    taille_ajustement = models.PositiveIntegerField(
        default=100, 
        help_text="En % : permet d'équilibrer les logos (ex: 80 pour un logo trop massif, 120 pour un logo trop fin)"
    )

    class Meta:
        ordering = ['ordre', 'nom']
        verbose_name = "Partenaire"

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        optimize_image_field(self.logo, max_dim=800, quality=85)
        super().save(*args, **kwargs)


class Replay(models.Model):
    invite = models.CharField(max_length=200, help_text="Nom de la personnalité (ex: Jean-Marc Jancovici)")
    url_youtube = models.URLField(help_text="Lien complet de la vidéo (ex: https://www.youtube.com/watch?v=...)")
    ordre = models.PositiveIntegerField(default=100, help_text="Plus petit nombre = apparaît en premier")

    class Meta:
        verbose_name = "Replay Vidéo"
        ordering = ['ordre', '-id']

    def __str__(self):
        return self.invite

    @property
    def video_id(self):
        regex = r"(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
        match = re.search(regex, self.url_youtube)
        return match.group(1) if match else None


# =====================================================================
# SIGNAUX : NETTOYAGE AUTOMATIQUE DU DISQUE (SUPPRESSION DES ANCIENS FICHIERS)
# =====================================================================
@receiver(post_delete, sender=Evenement)
@receiver(post_delete, sender=Membre)
@receiver(post_delete, sender=Partenaire)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Supprime le fichier du disque lors de la suppression d'un objet."""
    field_name = 'image' if sender == Evenement else ('photo' if sender == Membre else 'logo')
    file_field = getattr(instance, field_name, None)
    if file_field and file_field.name:
        try:
            file_field.delete(save=False)
        except Exception:
            pass


@receiver(pre_save, sender=Evenement)
@receiver(pre_save, sender=Membre)
@receiver(pre_save, sender=Partenaire)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Supprime l'ancien fichier du disque lorsqu'une nouvelle image est téléversée."""
    if not instance.pk:
        return

    field_name = 'image' if sender == Evenement else ('photo' if sender == Membre else 'logo')
    try:
        old_obj = sender.objects.get(pk=instance.pk)
        old_file = getattr(old_obj, field_name, None)
    except sender.DoesNotExist:
        return

    new_file = getattr(instance, field_name, None)
    if old_file and old_file.name and old_file != new_file:
        try:
            old_file.delete(save=False)
        except Exception:
            pass