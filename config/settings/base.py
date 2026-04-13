"""
Django settings for secretBox project.
"""

import os
from pathlib import Path
from config import env, get_version

VERSION = get_version()

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DEBUG")
BASE_DIR = Path(__file__).resolve().parent.parent.parent
TAILWIND_APP_NAME = 'theme'
if DEBUG:
    EXEMPLE_DEST = env("EXEMPLE_DEST")

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # "compressor",
]

PROJECT_APPS = [
    'account.apps.AccountConfig',
]

THIRD_PARTY_APPS = [
    # Tailwind
    'tailwind',
    'theme',
    'django_browser_reload',
    'crispy_forms']

DEV_APPS = [
    "django.test",
    "debug_toolbar",
]

INSTALLED_APPS = THIRD_PARTY_APPS + PROJECT_APPS + DJANGO_APPS 

if DEBUG:
    INSTALLED_APPS += DEV_APPS

DJANGO_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

TIERS_MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

MIDDLEWARE = TIERS_MIDDLEWARE + DJANGO_MIDDLEWARE

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"
AUTH_USER_MODEL = "account.MyUser"

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'theme/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "theme/static"),]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
COMPRESS_ENABLED = True
COMPRESS_ROOT = STATIC_ROOT

MEDIA_URL = 'media/'

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.ScryptPasswordHasher',
]


LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'login'
LOGIN_URL = 'login'