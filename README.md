# secretbox

## Description
petits outils d'organisation
- account : gestion des utilisateurs
- journaling : tableau de bord, organisation de vie
- jackietrade :  outil d'analyse boursière
- dictavoix : un outil d'aide à l'apprentissage des langues

## Maintenance

### Envoyer les modifications
make push
    - lance les tests
    - lance le contrôle qualité via ruff
    - effectue le commit
    - push les modifications

### Deploiement
- construire le zip avec make to-build
- si installation manuelle:
    - copier le zip dans le dossier hôte
    - lancer le script de déploiement : install.sh
    - verifier le service : systemctl status secretbox
    - en cas d'erreur, revoir les logs : 
        journalctl -u secretbox ou /var/log/secretbox/errors.log
- effectuer quelques manipulations en production

### Tagger la version après deploiement

- mettre à jour Readme.md
- git tag -a v0.0.0 -m "Version 0.0.0 : Création du projet"
- git push origin v0.0.0
- sauvegarde du code source: utils/save_src.sh
- sauvegarde de la base de données: utils/save_db.sh

### Retourner sur main et fusionner
git checkout main
git merge feature/ma-fonctionnalite

### Créer une branche feature
git checkout -b feature/ma-fonctionnalite

### Initialiser la nouvelle version
- mettre à jour VERSION + CHANGELOG

## Exploitation

### Creer le fichier .env
voir .env.example

### Exécuter des commandes Python
uv run python manage.py migrate
uv run python manage.py runserver (make run)

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

