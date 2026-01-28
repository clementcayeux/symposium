from django.urls import path
from . import views

urlpatterns = [
    # C'est cette ligne qui doit pointer vers views.index
    path('', views.index, name='index'), 
    
    path('equipe/', views.equipe, name='equipe'),
    path('contact/', views.contact, name='contact'),
    path('mentions-legales/', views.mentions_legales, name='mentions_legales'),
]