import os
import subprocess
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'symposium_site.settings')
django.setup()

from core.models import Invite
from datetime import datetime

print("Extraction des vidéos depuis @symposiumcs...")
# yt-dlp extrait métadonnées en json sans télécharger les vidéos
cmd = [
    "yt-dlp",
    "--flat-playlist",
    "-J",
    "https://www.youtube.com/@symposiumcs/videos"
]

res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
data = json.loads(res.stdout)

for entry in data.get('entries', []):
    titre = entry.get('title', '')
    url = f"https://www.youtube.com/watch?v={entry.get('id')}"
    
    # Extraction sommaire du nom (souvent au format "Conférence de [Nom] à CentraleSupélec")
    nom = titre.replace("Conférence de ", "").replace(" à CentraleSupélec", "").split("–")[0].strip()
    
    Invite.objects.get_or_create(
        youtube_url=url,
        defaults={
            'nom': nom[:200],
            'description': titre,
        }
    )

print("Import terminé avec succès !")