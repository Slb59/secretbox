# config.settings.dev.py

from config import env

from .base import *

DEBUG = True

ENVIRONMENT = "dev"

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
INTERNAL_IPS = [
    "127.0.0.1",
]

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
            "charset": "utf8mb4",  # Pour supporter les caractères spéciaux (émojis, etc.)
        },
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, "media")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
