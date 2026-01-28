from django.contrib import admin
from .models import Evenement
from django.utils import timezone


from .models import ContactRecipient

@admin.register(ContactRecipient)
class ContactRecipientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'actif')
    list_editable = ('actif',) # Permet de cocher/décocher direct dans la liste


@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    # On met à jour les noms des colonnes à afficher
    list_display = ('invite', 'titre', 'date_debut', 'display_statut')
    
    # On ne peut pas filtrer directement sur une @property (est_passe)
    # Donc on filtre plutôt par la date de début
    list_filter = ('categorie', 'date_debut', 'type_evenement')
    
    search_fields = ('invite', 'titre')

    # Petite fonction pour afficher le statut dans l'admin de façon propre
    def display_statut(self, obj):
        return "Passé" if obj.est_passe else "À venir"
    display_statut.short_description = "Statut"


from .models import Membre

@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    list_display = ('nom', 'role', 'ordre')
    list_editable = ('ordre',) # Permet de changer l'ordre directement dans la liste



from .models import ConfigurationSite

@admin.register(ConfigurationSite)
class ConfigurationSiteAdmin(admin.ModelAdmin):
    # Empêcher d'ajouter plusieurs lignes de config (Optionnel mais propre)
    def has_add_permission(self, request):
        return ConfigurationSite.objects.count() == 0
    


from .models import Partenaire

@admin.register(Partenaire)
class PartenaireAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ordre', 'taille_ajustement')
    list_editable = ('ordre', 'taille_ajustement')


from .models import Replay

@admin.register(Replay)
class ReplayAdmin(admin.ModelAdmin):
    list_display = ('invite', 'ordre', 'url_youtube')
    list_editable = ('ordre',)