import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Evenement, Membre, Partenaire

class Command(BaseCommand):
    help = "Supprime les fichiers orphelins dans MEDIA_ROOT qui ne sont plus référencés en base de données"

    def handle(self, *args, **options):
        # 1. Lister tous les fichiers référencés en base
        fichiers_actifs = set()

        for ev in Evenement.objects.all():
            if ev.image:
                fichiers_actifs.add(os.path.normpath(ev.image.path))

        for m in Membre.objects.all():
            if m.photo:
                fichiers_actifs.add(os.path.normpath(m.photo.path))

        for p in Partenaire.objects.all():
            if p.logo:
                fichiers_actifs.add(os.path.normpath(p.logo.path))

        # 2. Parcourir le dossier media réel
        media_root = settings.MEDIA_ROOT
        supprimes = 0
        octets_liberes = 0

        for root, dirs, files in os.walk(media_root):
            for file in files:
                filepath = os.path.normpath(os.path.join(root, file))
                if filepath not in fichiers_actifs:
                    taille = os.path.getsize(filepath)
                    os.remove(filepath)
                    octets_liberes += taille
                    supprimes += 1
                    self.stdout.write(f"Supprimé : {filepath}")

        mo_liberes = octets_liberes / (1024 * 1024)
        self.stdout.write(self.style.SUCCESS(
            f"Nettoyage terminé : {supprimes} fichier(s) orphelin(s) supprimé(s), {mo_liberes:.2f} Mo libérés."
        ))