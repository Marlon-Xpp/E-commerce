"""
Django settings for ecommers project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta  # Asegúrate de importar timedelta

import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', default='your secret key')

# SECURITY WARNING: don't run with debug turned on in production!
# Cambiar el debug a false para desplegarlo en heroku
DEBUG = 'RENDER' not in os.environ

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['*']

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:    
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


STATIC_URL = "/static/"

# Configuración de archivos estáticos para producción
if not DEBUG:
    # Cuando no estamos en DEBUG, configuramos STATIC_ROOT y el almacenamiento con WhiteNoise
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
else:
    # En desarrollo, se usan archivos estáticos desde el directorio 'static' en el proyecto
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
    
    
#configuracion de las api de mercado pago el key y el token
MERCADOPAGO_TEST_PUBLIC_KEY = 'TEST-c43be07b-ca92-44cd-88cb-87e640ac3dda'
MERCADOPAGO_TEST_ACCESS_TOKEN = 'TEST-5038588232712518-112923-a242cf4b6eff498c30e34d7c5f16bea1-1855980331'

# Configuración de correos electrónicos
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'mpillacap@autonoma.edu.pe')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '10216530')  # Usa una variable de entorno
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Configuraciones de autenticación
MAX_ATTEMPTS = 5  # Número máximo de intentos permitidos
BLOCK_TIME = timedelta(seconds=120)  # Tiempo de bloqueo de 15 segundos

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "products",
    "accounts",
    "payments",
    "main",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Agregar el whitenoise una ves instalado
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = "ecommers.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ecommers.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        default="postgresql://postgres:postgres@localhost/postgres",
        conn_max_age=600,
    )
    
    # esat es la configuracion para trabajr localmente con sqlite3 por defecto
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": BASE_DIR / "db.sqlite3",
    # }
}
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/



# STATIC_URL = "static/"
# # MEDIA_URL = "/uploads"
# # MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")

# # This production code might break development mode, so we check whether we're in DEBUG mode
# if not DEBUG:
#     # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
#     STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#     STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



# # CONFIGURACION PARA LOS ARCHIVOS  HEROKU
# STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# STATIC_TMP = os.path.join(BASE_DIR, "static")
# STATIC_URL = "/static/"

# os.makedirs(STATIC_TMP, exist_ok=True)
# os.makedirs(STATIC_ROOT, exist_ok=True)

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, "static"),
# )

# # Agregar esta configuracion de static storage
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

#20/10/30-mM*123456