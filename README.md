# secretbox

## Description
petits outils d'organisation
- account : gestion des utilisateurs
- journaling : tableau de bord
- jackietrade :  outil d'analyse boursière

## Maintenance
### Créer une branche feature
git checkout -b feature/ma-fonctionnalite

### Faire les modifications et commits
git add .
git commit -m "feat: Description de la fonctionnalité"

### Deploiement
- construire le zip avec make to-build
- copier le zip dans le dossier hôte
- lancer le script de déploiement : install.sh
- verifier le service : systemctl status secretbox
- en cas d'erreur, revoir les logs : journalctl -u secretbox

### Tagger la version après deploiement

- mettre à jour Readme.md
- git tag -a v0.0.0 -m "Version 0.0.0 : Création du projet"
- git push origin v0.0.0
- sauvegarde du code source: utils/save_src.sh
- sauvegarde de la base de données: utils/save_db.sh

### Retourner sur main et fusionner
git checkout main
git merge feature/ma-fonctionnalite

### Envoyer les modifications
git push origin HEAD

### Initialiser la nouvelle version
- mettre à jour VERSION + CHANGELOG

## Dépendances

Django 6.0.3
Django Tailwind 4.4.2
Django Debug Toolbar 6.3.0
MySQL (mysqlclient)

## Exploitation

### Creer le fichier .env
DEBUG=True
ALLOWED_HOSTS=localhost
DJANGO_SECRET_KEY=
DJANGO_SETTINGS_MODULE=config.settings.dev

DATABASE_URL=sqlite:///db.sqlite3

NPM_BIN_PATH=

DEFAULT_FROM_EMAIL=
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
ADMIN_EMAIL=


### Exécuter des commandes Python
uv run python manage.py migrate
uv run python manage.py runserver

### Lancer le shell Django
uv run python manage.py shell

## Base de données : Mariadb

### Activation / arrêt
sudo systemctl start mariadb
sudo systemctl stop mariadb
sudo systemctl status mariadb

### activation au demmarage
sudo systemctl enable mariadb

### Exporte/importe les données
/utils/save_db.sh
scp secretbox_dump.sql user@mint-pc:/tmp/ #copie sur cle pour mint
mariadb -u [user] -p secretbox_prod < /tmp/secretbox_dump.sql # deploiement sur mint

## Commandes reseau

### trouver l'ip local
ip a
hostname -I
ifconfig

### Ouvrir un port dans le pare-feu (UFW)
sudo ufw allow 3306/tcp  # MariaDB
sudo ufw allow 5432/tcp  # PostgreSQL
sudo ufw enable

## Liens utils

PostgreSQL : Documentation officielle : https://www.postgresql.org/docs/

MariaDB :
Documentation MariaDB : https://mariadb.com/kb/en/
Configuration sous Arch Linux : https://wiki.archlinux.org/title/MariaDB

Django :
Documentation Django : https://docs.djangoproject.com/fr/4.2/
Tutoriel officiel : https://docs.djangoproject.com/fr/4.2/intro/tutorial01/

Raspberry Pi :
Documentation officielle : https://www.raspberrypi.org/documentation/
Installation d’Ubuntu Server : https://ubuntu.com/tutorials/how-to-install-ubuntu-on-your-raspberry-pi

