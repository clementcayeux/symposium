from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('equipe/', views.equipe, name='equipe'), # La page "Nous connaître"
    path('contact/', views.contact, name='contact'), # La nouvelle page Contact
]