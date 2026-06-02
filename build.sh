#!/usr/bin/env bash
set -e

APP_NAME="secretbox"
BASE_DIR="$PWD"
BUILD_DIR="$BASE_DIR/build"

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

echo "▶ Nettoyage avant build"
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR/app"
chmod 755 "$BUILD_DIR/app" "$BUILD_DIR"

echo "▶ Copie des fichiers applicatifs dans $BUILD_DIR/app"
rsync -av --exclude-from='.buildignore' ./ "$BUILD_DIR/app/"

echo "▶ Copie des fichiers d'installation "
cp install.sh "$BUILD_DIR"
cp VERSION "$BUILD_DIR"
cp makefile-prod "$BUILD_DIR"/app/makefile

echo "▶ Création de l’archive $VERSION dans build"
cd "$BUILD_DIR/app"
7z a "$BUILD_DIR"/"app.7z" .
ARCHIVE_NAME="$VERSION"_"$APP_NAME"_"$(date +%Y.%m.%d)"_linux
GLOBAL_ARCHIVE_NAME="$BUILD_DIR"/"$ARCHIVE_NAME".7z
echo "global archive name $GLOBAL_ARCHIVE_NAME"
7z a "$GLOBAL_ARCHIVE_NAME" "$BUILD_DIR"/VERSION
7z a "$GLOBAL_ARCHIVE_NAME" "$BUILD_DIR"/install.sh
7z a "$GLOBAL_ARCHIVE_NAME" "$BUILD_DIR"/"app.7z"

echo "✔ Archive de téléchargement créée : $GLOBAL_ARCHIVE_NAME"
read -rp "Voulez-vous procéder à l'installation ? [O/n] " REPONSE

case "$REPONSE" in
    ""|[Oo])
        cd "$BASE_DIR"
        set -a
        source .env
        set +a
        echo "cp '$GLOBAL_ARCHIVE_NAME' '$EXEMPLE_DEST'"
        cp "$GLOBAL_ARCHIVE_NAME" "$EXEMPLE_DEST"
        echo "cd '$EXEMPLE_DEST'"
        cd "$EXEMPLE_DEST"
        7z x "$ARCHIVE_NAME".7z -y
        echo "Installation de l'application..."
        sudo ./install.sh
        ;;
    [Nn])
        echo "Annulé."
        exit 0
        ;;
    *)
        echo "Réponse invalide."
        exit 1
        ;;
esac



