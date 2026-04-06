# secretbox
personnal organisation tools



## Maintenance
- git add .
- git commit -m "Ajout de la nouvelle API d'utilisateurs
> Description détaillée des changements
> Impact sur le système existant"
- git push origin HEAD

- mettre à jour Readme.md + VERSION
- git tag -a v0.0.0 -m "Version 0.0.0 : Création du projet"
- git push origin v0.0.0
- sauvegarde du code source: gitingest . -o tests/output/digest.txt -i "*.py *.css *.js"

### création d'une branche pour une nouvelle fonctionnalité
git checkout -b feature/objectif
git commit -m "feat: Ajout de la nouvelle fonctionnalité"
git checkout main
git merge feature/objectif

### Mise à jour depuis la branche principale
git fetch upstream
git rebase upstream/main

### Créer une release
- git tag -a v0.0.0 -m "Version 0.0.0 : Création du projet"
- git push origin v0.0.0