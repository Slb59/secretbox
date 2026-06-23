# config.settings.prod.py
from .base import *

DEBUG = False

ENVIRONMENT = "prod"

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("BASE_NAME"),  # Nom de votre base
        "USER": env("BASE_USER"),  # Utilisateur MariaDB
        "PASSWORD": env("BASE_PWD"),  # Mot de passe de l'utilisateur
        "HOST": env("BASE_HOST"),  # Adresse IP du serveur MariaDB
        "PORT": env("BASE_PORT"),  # Port par défaut de MariaDB
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            # Pour supporter les caractères spéciaux (émojis, etc.)
            "charset": "utf8mb4",  
        },
    }
}

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# doit être modifié si déploiement sur serveur web
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
INTERNAL_IPS = [
    "127.0.0.1",
]

MEDIA_ROOT = os.path.join("/var/lib/secretbox/", "media")

NPM_BIN_PATH = env("NPM_BIN_PATH")


LOGGING = {
    "version": 1,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": "/var/log/secretbox/errors.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
        },
    },
}

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
