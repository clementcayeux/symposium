from django.db import models    

class Evenement(models.Model):
    invite = models.CharField(max_length=200) # Ex: Manuel Bompard
    titre = models.CharField(max_length=200)  # Ex: Souveraineté et défis...
    categorie = models.CharField(max_length=100, default="Politique") # Ex: Politique
    date_evenement = models.DateTimeField()
    lieu = models.CharField(max_length=200, default="Amphi Michelin") # Ex: Amphi Michelin
    image = models.ImageField(upload_to='evenements/')
    est_passee = models.BooleanField(default=False)

    def __str__(self):
        return self.invite
    
    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
    

class ContactRecipient(models.Model):
    nom = models.CharField(max_length=100, help_text="Nom du membre")
    email = models.EmailField()
    actif = models.BooleanField(default=True, help_text="Décocher pour ne plus recevoir les mails temporairement")

    def __str__(self):
        return f"{self.nom} ({self.email})"

    class Meta:
        verbose_name = "Destinataire des messages du formulaire"
        verbose_name_plural = "Destinataires des messages du formulaire"