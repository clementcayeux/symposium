from django.contrib import admin
from .models import Conference

@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('invite', 'titre', 'date_evenement', 'est_passee')
    list_filter = ('est_passee',)


from .models import ContactRecipient

@admin.register(ContactRecipient)
class ContactRecipientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'actif')
    list_editable = ('actif',) # Permet de cocher/décocher direct dans la liste