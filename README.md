Symposium CentraleSupélec — Site Officiel

Bienvenue sur le dépôt du site officiel de Symposium CentraleSupélec.

Ce site a vocation à servir de vitrine pour l’association : présentation des conférences, de l’équipe, et mise à disposition d’un formulaire de contact.

Stack technique

Framework : Django 5.x (Python)

Frontend : HTML5, CSS3 (Grid & Flexbox custom), JavaScript vanilla

Emails : Relais SMTP via Brevo

Design : Responsive (mobile first), aux couleurs Navy & Or de Symposium

Structure du projet
├── symposium_site/          # Configuration Django (settings, urls)
├── core/                    # Application principale
│   ├── static/core/         # CSS, JavaScript et assets (images, favicon)
│   ├── templates/core/      # Templates HTML
│   │   └── emails/          # Templates HTML des emails
│   ├── views.py             # Logique des pages et formulaire de contact
│   └── urls.py              # Routage des pages
├── manage.py                # Point d’entrée des commandes Django
└── db.sqlite3               # Base de données (sessions et messages)

Installation locale (développement)
1. Cloner le dépôt
git clone https://gitlab-cw4.centralesupelec.fr/clement.cayeux/symposium.git
cd symposium_site

2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate     # Windows : venv\Scripts\activate

3. Installer les dépendances
pip install django

4. Appliquer les migrations
python manage.py migrate

5. Lancer le serveur de développement
python manage.py runserver


Le site est alors accessible à l’adresse :
http://127.0.0.1:8000

Configuration du formulaire de contact (Brevo)

Le formulaire de contact utilise Brevo pour l’envoi des emails, afin d’éviter les blocages SMTP liés à Outlook ou Gmail.

Dans settings.py, vérifier les paramètres suivants :

EMAIL_HOST_USER
Adresse email du compte Brevo (ex. formulaire.symposium@outlook.com)

EMAIL_HOST_PASSWORD
Clé SMTP Master générée depuis le dashboard Brevo

DEFAULT_FROM_EMAIL
Adresse d’expédition affichée aux utilisateurs

Maintenance et mises à jour
Modifier l’équipe

Fichier :
core/templates/core/equipe.html

Photos :
À placer dans static/core/assets/
Formats recommandés : .jpg ou .png (de préférence carrés)

Emails :
Les adresses individuelles ont été volontairement supprimées pour éviter le scraping.
Privilégier les liens LinkedIn et le formulaire de contact.

Modifier les destinataires du formulaire de contact

Dans views.py, fonction contact, mettre à jour la liste :

recipient_list = [
    'clement.cayeux@symposium-cs.fr',
    ...
]


Tous les messages envoyés via le formulaire seront transmis à ces adresses.

Mettre à jour les prochaines conférences

Fichier :
core/templates/core/index.html

Photos :
À placer dans static/core/assets/
Formats recommandés : .jpg ou .png

Ajouter ou modifier les replays

Les liens YouTube se modifient directement dans index.html, dans la section Replays.

Mentions légales

Le texte est conforme à la loi LCEN.
En cas de changement d’hébergeur ou de président de l’association, mettre à jour :

mentions_legales.html

Contact en cas de problème

Développeur original : Clément Cayeux (mandat 2026)

Hébergement : ViaRezo