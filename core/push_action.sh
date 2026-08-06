#!/usr/bin/env bash
set -e

# Créer un fichier log avec timestamp
LOG_FILE="./output/error_log_$(date +%Y%m%d_%H%M%S).log"

echo "▶ lancement des tests"	
# uv run manage.py test >> "$LOG_FILE"
# npx playwright test >> "$LOG_FILE"

echo "▶ contrôle qualité"
uv run ruff check . >> "$LOG_FILE"
uv run ruff format . >> "$LOG_FILE"

echo "▶ execution du commit"
read -rp "Veuillez commenter le commit: " REPONSE
echo

git add .
git commit -m "$REPONSE" >> "$LOG_FILE"
git push origin HEAD >> "$LOG_FILE"

# Afficher le chemin du fichier log à la fin
echo ""
echo "✓ Push complété"
echo "Fichier d'erreurs: $LOG_FILE"

#	automatiser 4 sauvegarde de base hebdomadaires + 6 mensuels