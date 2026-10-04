from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import admin_entry_redirect

urlpatterns = [
    # On intercepte les anciennes URLs admin pour forcer le nouveau design
    path('admin/login/', admin_entry_redirect),
    path('admin/', admin_entry_redirect),
    
    # Accès de secours au vieux backend (à garder secret : /admin/django-backend/)
    path('admin/django-backend/', admin.site.urls), 

    # Inclusion des URLs du site (qui contient la route /connexion/)
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)