
from pathlib import Path
import os
from datetime import timedelta  # Asegúrate de importar timedelta
import cloudinary
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CHARSET = 'utf-8'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', default='blablablabla12')

# SECURITY WARNING: don't run with debug turned on in production!
# Cambiar el debug a false para desplegarlo 
DEBUG = 'RENDER' not in os.environ

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = []  

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


#configuracion de las api de mercado pago el key y el token
MERCADOPAGO_TEST_PUBLIC_KEY = 'TEST-c43be07b-ca92-44cd-88cb-87e640ac3dda'
MERCADOPAGO_TEST_ACCESS_TOKEN = 'TEST-5038588232712518-112923-a242cf4b6eff498c30e34d7c5f16bea1-1855980331'

# Configuración de correos electrónicos
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'gs772918@gmail.com') # Correo
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'ftvo inro lcss eyqu')  # Contra
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
    "cloudinary",  # 👈 añadido para cloudinary
    "cloudinary_storage",  # 👈 añadido para cloudinary
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # 👈 añadido el whiteNoiseMideeleware
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ecommers.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
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

# BD SQLITE3 LOCAL
DATABASES = {
    # esta es la configuracion para trabajar localmente con sqlite3 por defecto
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }    
}

# BD POSTGRES REMOTO
# DATABASES = {
#     # esta configuracion es cuando se conecta de manera remota a la bd con postgres 
#     "default": dj_database_url.config(
#         default="postgresql://freccardi:9pcxccmsXoyU4UVf41CnmfnJgQ3nkuLS@dpg-d0ibnhnfte5s73fpnf70-a.oregon-postgres.render.com/bd_freccardi",
#         conn_max_age=600,
#     )
# }


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

LANGUAGE_CODE = "es"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (IMÁGENES SUBIDAS POR EL USUARIO)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')  # ❌ Ya no se usa, porque usas Cloudinary

# Configuración de Cloudinary
# cloudinary.config(
#     cloud_name='duv5jc1d0',  # Tu nombre de la nube de Cloudinary
#     api_key='561134372158658',  # Tu API Key de Cloudinary
#     api_secret='neo6ehkdBBVnaMC9lPZc-D-iPx8'  # Tu API Secret de Cloudinary
# )

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Producción en Render con whitenoise
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"