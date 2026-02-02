# Symposium CentraleSupélec - Site Officiel

Bienvenue sur le dépôt du site officiel de **Symposium**. Ce site a été conçu comme la vitrine de l'association : il permet de présenter les conférences, l'équipe actuelle et centralise la prise de contact via un formulaire sécurisé.

## Aidez vous de l'IA pour vous expliquer et vous écrire les codes !

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

(ou plutôt avec la clé SSH git@gitlab-cw4.centralesupelec.fr:clement.cayeux/symposium.git)


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



Symposium - https://symposium-cs.fr/
[Dernière mise à jour : Janvier 2026 (création du nouveau site)]
Mots de passe en bas
Ce site a été conçu pour être la vitrine de l'association, permettant de présenter les conférences, l'équipe et de faciliter la prise de contact.


Mises à jour du site

Se connecter à la page d’admin Django pour modifier le site sans passer par le code html https://symposium-cs.fr/admin (mettre à la fin de l’url :    /admin)  [voir codes en dessous]. D’ici on peut modifier facilement : 
la date du mandat (dans configuration du site)
les membres du mandat
les prochains événements (3 premiers affichés seulement)
les replays (3 premiers affichés seulement)
les partenaires

Tout le reste se gère directement dans le html. Il faut utiliser git, travailler dans VScode en local puis mettre à jour le serveur avec la nouvelle version.
Penser aux mentions Légales : Si l'hébergeur est modifié, mettre à jour mentions_legales.html


Stack Technique
Framework : Django 5.x (Python)
Frontend : HTML5, CSS3 (Custom Grid & Flexbox), JavaScript Vanilla
Emails : Microsoft 365 (SMTP Authenticated).
Design : Responsive (Mobile First) aux couleurs Navy & Or de Symposium
Hébergement : VM Debian (Serveur dédié/VPS), par ViaRezo
Serveur Web : Nginx (Reverse Proxy).
Base de données : PostgreSQL.
Analytics : Umami (Self-hosted via Docker).

Structure du Projet


Installation Locale (Développement)
Pour reprendre le projet sur votre machine (DANS VS CODE) :
Cloner le dépôt :
git clone https://gitlab-cw4.centralesupelec.fr/clement.cayeux/symposium.git
cd symposium_site
Créer un environnement virtuel :
python -m venv venv
source venv/bin/activate (sur Windows : venv\Scripts\activate)
installer toutes les bibliothèques nécessaires, elles sont dans requirements.txt : 
python3 -m pip install -r requirements.txt
Appliquer les migrations :
python manage.py migrate
Lancer le serveur en local :
python manage.py runserver


Infrastructure & Serveur (La VM ViaRezo)
Accès
Connexion : ssh debian@ip_du_serveur
Gestionnaire de processus : Gunicorn (servi par Nginx).
Nginx & SSL
Les fichiers de configuration se trouvent dans /etc/nginx/sites-available/.
symposium : Gère le site principal.
umami : Gère le sous-domaine stats.symposium-cs.fr.
SSL : Géré par Certbot (Let's Encrypt). Renouvellement automatique via cron.


Configuration du Formulaire de Contact
Le site utilise contact@symposium-cs.fr pour l'envoi des mails, voir settings.py

Gestion des Emails
Configuration : Les paramètres SMTP sont dans le .env de Django.
Note de sécurité : Les "Security Defaults" de Microsoft 365 ont été désactivés pour permettre l'envoi SMTP. Ne jamais les réactiver sans configurer une alternative (OAuth2), sinon l'envoi de mail cassera.
MFA : Le compte d'envoi utilise un "Mot de passe d'application" par l’adresse clement.cayeux@symposium-cs.fr (attention ne pas enlever les autorisations à cette adresse, laisser le MFA activé.

Statistiques & RGPD (Umami)
Localisation dans la VM : ~/umami/
Techno : Docker Compose.
Maintenance : Pour mettre à jour Umami, aller dans le dossier et faire :
Bash
sudo docker compose pull
sudo docker compose up -d
RGPD : Tant qu'Umami est utilisé seul, aucun bandeau de cookies n'est requis.

Checklist de Maintenance Annuelle
Chaque nouvelle équipe doit vérifier ces points en septembre :
Renouvellement du Domaine : Vérifier la date d'expiration.
Certificats SSL : Vérifier avec sudo certbot certificates.
Mises à jour :
sudo apt update && sudo apt upgrade (Système).
pip install --upgrade -r requirements.txt (Django).
Mots de passe : Changer les mots de passe du dashboard Umami et de la base de données s'il y a eu des départs sensibles.
Logs : Vérifier les erreurs dans /var/log/nginx/error.log.

En cas de crash (Dépannage rapide)
Le site affiche 502 Bad Gateway : Gunicorn est probablement arrêté.
sudo systemctl restart gunicorn
Les mails ne partent plus : Souvent dû à un changement de politique de sécurité Microsoft ou un mot de passe expiré.
Vérifier les logs Django.
Les stats ne s'affichent plus : Le container Docker est peut-être tombé.
cd ~/umami && sudo docker compose restart


Sécurité & Confidentialité
⚠️ RÈGLE D'OR : Le dépôt GitLab doit impérativement rester en PRIVÉ. Le fichier .env ne doit jamais être commité sur Git (il contient la secret key django et le mot de passe d’application du compte mail microsoft pour le formulaire).


Contact & Hébergement
Développeur Original : Clément Cayeux (Mandat 2026)
Hébergement : ViaRezo (CentraleSupélec)
Registrar (Domaine) : Microsoft 365 (compte des adresses sympo)
