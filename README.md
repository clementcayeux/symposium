# Symposium CentraleSupélec - Site Officiel

Bienvenue sur le dépôt du site officiel de **Symposium**. Ce site a été conçu comme la vitrine de l'association : il permet de présenter les conférences, l'équipe actuelle et centralise la prise de contact via un formulaire sécurisé.

---

##  Stack Technique

* **Framework :** Django 5.x (Python)
* **Frontend :** HTML5, CSS3 (Custom Grid & Flexbox), JavaScript Vanilla
* **Emails :** Relais SMTP via **Brevo**
* **Design :** Responsive (Mobile First) aux couleurs Navy & Or du Symposium.

---

##  Structure du Projet

```plaintext
├── symposium_site/          # Dossier de configuration Django (settings, urls)
├── core/                    # Application principale (le coeur du site)
│   ├── static/core/         # Fichiers CSS, JS et Assets (Images, Favicon)
│   ├── templates/core/      # Fichiers HTML
│   │   └── emails/          # Templates HTML pour les mails de confirmation
│   ├── views.py             # Logique des pages et du formulaire de contact
│   └── urls.py              # Routage des pages
├── manage.py                # Point d'entrée des commandes Django
└── db.sqlite3               # Base de données (sessions et messages flash)

```


##  Installation Locale (Développement)
Pour reprendre le projet sur votre machine :

Cloner le dépôt :

Bash

git clone [https://gitlab-cw4.centralesupelec.fr/clement.cayeux/symposium.git](https://gitlab-cw4.centralesupelec.fr/clement.cayeux/symposium.git)
cd symposium_site
Créer un environnement virtuel :

Bash

python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
Installer Django :

Bash

pip install django
Appliquer les migrations :

Bash

python manage.py migrate
Lancer le serveur :

Bash

python manage.py runserver


##  Configuration du Formulaire de Contact (Brevo)
Le site utilise Brevo pour l'envoi des mails afin d'éviter les blocages SMTP classiques des boîtes Outlook/Gmail.

Paramètres à vérifier dans settings.py :
EMAIL_HOST_USER : L'adresse email du compte Brevo (formulaire.symposium@outlook.com).

EMAIL_HOST_PASSWORD : La Clé SMTP Master générée sur le dashboard Brevo (onglet SMTP & API).

DEFAULT_FROM_EMAIL : L'adresse d'expédition qui apparaîtra chez le destinataire.

## 🔧 Maintenance & Mises à jour

### Modifier l'Équipe
Les membres sont gérés manuellement dans core/templates/core/equipe.html.

Photos : À placer dans static/core/assets/. Format recommandé : .jpg ou .png (format carré de préférence).

Sécurité : Les emails individuels sont masqués pour éviter le "scraping". Utilisez les liens LinkedIn.

### Modifier les destinataires du formulaire
Pour changer qui reçoit les messages envoyés via le site :

Ouvrir core/views.py.

Dans la fonction contact, modifier la recipient_list :

Python

recipient_list=['clement.cayeux@symposium-cs.fr', 'autre.membre@symposium-cs.fr']

### Mettre à jour les conférences
Directement dans core/templates/core/index.html.

Modifier les textes et les sources d'images (static/core/assets/).

### Ajouter des Replays
Les liens YouTube se modifient dans index.html au niveau de la section "Replays". Il suffit de remplacer l'ID de la vidéo dans l'URL d'intégration.

### Mentions Légales
Le texte est conforme à la loi LCEN. Si le Président de l'association change ou si l'Hébergeur est modifié, mettez à jour le fichier mentions_legales.html.

### Contact & Hébergement
Développeur Original : Clément Cayeux (Mandat 2026)

Hébergement : ViaRezo (CentraleSupélec)

Dernière mise à jour : Janvier 2026