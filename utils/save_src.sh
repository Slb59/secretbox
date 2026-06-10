#!/usr/bin/env bash

set -a
source .env
set +a

echo "Répertoire des sauvegardes : $BACKUPS"
mkdir -p "$BACKUPS"

set -e

# Lire la version
if [[ ! -f VERSION ]]; then
  echo "❌ Fichier VERSION introuvable"
  exit 1
fi

VERSION="$(tr -d '[:space:]' < VERSION)"

if [[ -z "$VERSION" ]]; then
  echo "❌ VERSION est vide"
  exit 1
fi

uv run gitingest .. \
  -o "$BACKUPS"/digest-"$VERSION".txt \
  -i "*.py,*.css,*.js,*.html"