#!/usr/bin/env bash
set -e

# ------------------------------------------------------------------------------
# Variables d'environnement
# ------------------------------------------------------------------------------

APP_PORT="9000"
APP_NAME="secretbox"
APP_USER="root"
APP_BASE="/opt/secretbox"
DATA_DIR="/var/lib/secretbox"
APP_DIR="$APP_BASE/app"
VENV_DIR="$APP_DIR/.venv"
export UV_HTTP_TIMEOUT=240


echo "▶ Installation de $APP_NAME"

# ------------------------------------------------------------------------------
# Vérifications
# ------------------------------------------------------------------------------
if [ "$EUID" -ne 0 ]; then
  echo "❌ Ce script doit être lancé en root (sudo)"
  exit 1
fi

command -v python3 >/dev/null || {
  echo "❌ Python 3 requis"
  exit 1
}

# ------------------------------------------------------------------------------
# Utilisateur système
# ------------------------------------------------------------------------------
if ! id "$APP_USER" >/dev/null 2>&1; then
  echo "▶ Création de l'utilisateur système $APP_USER"
  useradd --system --home "$APP_BASE" --shell /usr/sbin/nologin "$APP_USER"
fi

rm -rf "$VENV_DIR" 
rm -rf "$APP_DIR"
mkdir -p "$APP_DIR" "$DATA_DIR" "$DATA_DIR/media" "$VENV_DIR" 
chown -R "$APP_USER:$APP_USER" "$APP_BASE"
chown -R "$APP_USER:$APP_USER" $DATA_DIR/media/

# ------------------------------------------------------------------------------
# Installation de uv
# ------------------------------------------------------------------------------
if ! command -v uv >/dev/null; then
  echo "▶ Installation de uv"
  curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh
fi

# ------------------------------------------------------------------------------
# Copie du projet
# ------------------------------------------------------------------------------
echo "▶ Copie du projet"
# rsync -av --delete --exclude-from='.installignore' ./ "$APP_DIR/"
BASE_NAME="${DATA_DIR}/db.sqlite3"
if [ -f "${BASE_NAME}" ]; then
  cp "${BASE_NAME}" "${BASE_NAME}.${VERSION}.back"
  echo "▶ Fichier de base de données trouvé, une sauvegarde est créée dans ${BASE_NAME}.${VERSION}.back"
fi
VERSION="$(tr -d '[:space:]' < VERSION)"
ARCHIVE_NAME="${APP_NAME}-${VERSION}.7z"
echo "▶ Extraction de l'archive"
sudo 7z x "app.7z" -o"$APP_DIR" -y

# ------------------------------------------------------------------------------
# Environnement Python
# ------------------------------------------------------------------------------
echo "▶ Création du venv"
chown -R "$APP_USER:$APP_USER" "$APP_BASE"
chmod -R 755 "$APP_BASE"
sudo -u "$APP_USER" uv venv "$VENV_DIR" --clear
chown -R "$APP_USER:$APP_USER" "$VENV_DIR"

echo "▶ Nettoyage du cache Python depuis $APP_DIR"
cd "$APP_DIR"
source .venv/bin/activate
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

echo "▶ Installation des dépendances Python"
uv sync --refresh

# ------------------------------------------------------------------------------
# Création du fichier d'environnement
# ------------------------------------------------------------------------------
echo "▶ Création du .env"
if [ ! -f "$DATA_DIR/.env" ]; then
    echo "Création du .env production"
    NEWKEY=$("./djangokey.sh")
    cat > "$DATA_DIR/.env" <<EOF
DEBUG=False
ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_SECRET_KEY=$NEWKEY
DATABASE_URL=sqlite:////$DATA_DIR/db.sqlite3
NPM_BIN_PATH=/////usr/lib/node_modules/npm
EOF
  chown "$APP_USER:$APP_USER" "$DATA_DIR/.env"
  chmod 600 "$DATA_DIR/.env"
fi
ENV_FILE=$DATA_DIR/.env

# ------------------------------------------------------------------------------
# Base de données
# ------------------------------------------------------------------------------
echo "▶ Migrations Django"
export DJANGO_SETTINGS_MODULE=config.settings.prod
DJANGO_SUPERUSER_USERNAME=$SUPERUSER_USERNAME
DJANGO_SUPERUSER_EMAIL=$SUPERUSER_EMAIL
DJANGO_SUPERUSER_PASSWORD=$SUPERUSER_PASSWORD

cd $APP_DIR
uv run manage.py migrate --noinput
uv run manage.py tailwind build
uv run manage.py collectstatic --noinput

# ------------------------------------------------------------------------------
# Création du service systemd secretbox.service
# ------------------------------------------------------------------------------
echo "▶ Installation du service systemd"

cat > /etc/systemd/system/secretbox.service <<EOF
[Unit]
Description=SecretBox (Django)
After=network.target

[Service]
User=$APP_USER
WorkingDirectory=$APP_DIR
ExecStart=$VENV_DIR/bin/gunicorn --bind 127.0.0.1:9000 config.wsgi:secretbox
Restart=always
EnvironmentFile=$DATA_DIR/.env
Environment=ENV_FILE=$DATA_DIR/.env
Environment=DJANGO_SETTINGS_MODULE=config.settings.prod

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable secretbox
systemctl restart secretbox
systemctl status secretbox

uv run manage.py showmigrations

# ------------------------------------------------------------------------------
# Récapitulatif de fin
# ------------------------------------------------------------------------------
echo
echo "✅ SecretBox est installé et démarré"
echo "🌐 Ouvrir : http://localhost:$APP_PORT"
echo "📋 Statut : systemctl status SecretBox"
