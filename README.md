# Symposium



## Initialisation



## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab-cw4.centralesupelec.fr/clement.cayeux/symposium/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/user/project/merge_requests/auto_merge/)



# Symposium CentraleSupélec - Site Officiel
Bienvenue sur le dépôt du site officiel de Symposium. Ce site a été conçu pour être vitrine de l'association, permettant de présenter les conférences, l'équipe et de faciliter la prise de contact.

Stack Technique
Framework : Django 5.x (Python)

Frontend : HTML5, CSS3 (Custom Grid & Flexbox), JavaScript Vanilla

Emails : Relais SMTP via Brevo


Design : Responsive (Mobile First) aux couleurs Navy & Or du Symposium.

📂 Structure du Projet
Plaintext

├── symposium_site/          # Dossier de configuration Django (settings, urls)
├── core/                    # Application principale
│   ├── static/core/         # Fichiers CSS, JS et Assets (Images, Favicon)
│   ├── templates/core/      # Fichiers HTML
│   │   └── emails/          # Templates HTML pour les envois de mails
│   ├── views.py             # Logique des pages et du formulaire de contact
│   └── urls.py              # Routage des pages
├── manage.py                # Point d'entrée des commandes Django
└── db.sqlite3               # Base de données (utilisée pour les sessions/messages)



Installation Locale (Développement)
Pour reprendre le projet sur votre machine :

Cloner le dépôt :



Bash

git clone https://gitlab-cw4.centralesupelec.fr/clement.cayeux/symposium.git
cd symposium_site
Créer un environnement virtuel :

Bash

python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
Installer les dépendances :

Bash

pip install django
Appliquer les migrations :

Bash

python manage.py migrate
Lancer le serveur :

Bash

python manage.py runserver


Configuration du Formulaire de Contact (Brevo)
Le site utilise Brevo pour l'envoi des mails afin d'éviter les blocages SMTP d'Outlook/Gmail.

Paramètres à vérifier dans settings.py :
EMAIL_HOST_USER : L'adresse email du compte Brevo (formulaire.symposium@outlook.com).

EMAIL_HOST_PASSWORD : La Clé SMTP Master générée sur le dashboard Brevo.

DEFAULT_FROM_EMAIL : L'adresse d'expédition affichée aux utilisateurs.


Maintenance & Mises à jour
1. Modifier l'Équipe
Les membres sont gérés directement dans le template core/templates/core/equipe.html.

Photos : À placer dans static/core/assets/. Format recommandé : .jpg ou .png (carré de préférence).

Emails : Par sécurité, les emails individuels ont été retirés pour éviter le "scraping". Privilégiez les liens LinkedIn et le formulaire Contact


2. Modifier les adresses emails du formulaire Contact : dans views.py -> def(contact) -> Utilisateurs send(mail), il faut mettre à jour la liste :
recipient_list=['clement.cayeux@symposium-cs.fr',...]
qui contient les emails à qui tout message du questionnaire est transmis.

3. Mettre à jour les prochaine conférences
Directement dans core/templates/core/index.html

Photos : À placer dans static/core/assets/. Format recommandé : .jpg ou .png 

4. Ajouter des Replays
Les liens YouTube se modifient dans index.html au niveau de la section "Replays".

5. Mentions Légales
Le texte est conforme à la loi LCEN. Si l'hébergeur ou le Président change, mettez à jour mentions_legales.html.



Contact en cas de pépin
Développeur Original : Clément Cayeux (Mandat 2026)

Hébergement : ViaRezo