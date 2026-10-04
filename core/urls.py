from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Pages publiques
    path('', views.index, name='index'), 
    path('equipe/', views.equipe, name='equipe'),
    path('contact/', views.contact, name='contact'),
    path('mentions-legales/', views.mentions_legales, name='mentions_legales'),

    # Authentification sur mesure (CMS)
    path('connexion/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('deconnexion/', views.custom_logout, name='logout'),

    # Tableau de bord des réglages
    path('reglages/', views.reglages, name='reglages'),

    # API AJAX pour l'inline editing & gestion directe
    path('api/save-item/', views.api_save_item, name='api_save_item'),
    path('api/delete-item/', views.api_delete_item, name='api_delete_item'),
]