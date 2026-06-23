#!/usr/bin/env bash
set -e

echo "▶ lancement des tests"	
# uv run manage.py test
# npx playwright test

echo "▶ contrôle qualité"
uv run ruff check .
uv run ruff format .

echo "▶ execution du commit"
read -rp "Veuillez commenter le commit: " REPONSE

git add .
git commit -m "$REPONSE"
git push origin HEAD

#	automatiser 4 sauvegarde de base hebdomadaires + 6 mensuels