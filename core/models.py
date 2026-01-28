from django.db import models    
from django.utils import timezone

class Evenement(models.Model):
    # Types d'événements pour filtrer facilement
    TYPE_CHOICES = [
        ('CONF', 'Conférence'),
        ('TABLE', 'Table Ronde'),
        ('WORK', 'Atelier / Workshop'),
        ('HACK', 'Hackathon'),
        ('TRIP', 'Voyage d\'étude'),
        ('AUTRE', 'Autre'),
    ]

    invite = models.CharField(max_length=200, help_text="Nom de l'intervenant ou nom du projet")
    titre = models.CharField(max_length=400, help_text="Description")
    categorie = models.CharField(max_length=100, default="Politique",help_text="Le petit texte couleur or")
    type_evenement = models.CharField(max_length=10, choices=TYPE_CHOICES, default='CONF')
    
    # Gestion du temps (Flexible)
    date_debut = models.DateTimeField(verbose_name="Date et heure de début")
    date_fin = models.DateTimeField(null=True, blank=True, verbose_name="Date et heure de fin (optionnel)")
    horaires_precision = models.CharField(max_length=100, blank=True, help_text="Ex: 'Toute la journée' ou '14h-18h'")
    
    lieu = models.CharField(max_length=200, default="Amphi Michelin")
    image = models.ImageField(upload_to='evenements/')
    lien_inscription = models.URLField(blank=True, null=True, help_text="Lien vers la billetterie (Lydia, Shotgun, etc.)")
    
    # Statut
    est_publie = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Événement"
        ordering = ['-date_debut']

    def __str__(self):
        return f"{self.invite} - {self.titre}"

    @property
    def est_passe(self):
        """Calcule automatiquement si l'événement est terminé de façon sécurisée"""
        # 1. On détermine la date de référence (fin si elle existe, sinon début)
        date_reference = self.date_fin if self.date_fin else self.date_debut

        # 2. Sécurité : Si pour une raison X ou Y, aucune date n'est définie
        if not date_reference:
            return False

        # 3. Comparaison sécurisée
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
        ordering = ['ordre', 'nom'] # Tri automatique par ordre

    def __str__(self):
        return f"{self.nom} ({self.role})"
    

class ConfigurationSite(models.Model):
    annee_promotion = models.CharField(max_length=4, default="2026", help_text="L'année affichée pour l'équipe (ex: 2026)")
    # Tu pourras ajouter d'autres champs ici plus tard (ex: slogan, lien réseaux sociaux)

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
    
    # Le réglage magique pour l'admin
    taille_ajustement = models.PositiveIntegerField(
        default=100, 
        help_text="En % : permet d'équilibrer les logos (ex: 80 pour un logo trop massif, 120 pour un logo trop fin)"
    )

    class Meta:
        ordering = ['ordre', 'nom']
        verbose_name = "Partenaire"

    def __str__(self):
        return self.nom
    


import re

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
        """Extrait l'ID de la vidéo YouTube pour la miniature"""
        regex = r"(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
        match = re.search(regex, self.url_youtube)
        return match.group(1) if match else None