import os
from pathlib import Path
from decouple import config
import dj_database_url

# Diretório base
BASE_DIR = Path(__file__).resolve().parent.parent

# Segurança
SECRET_KEY = config('SECRET_KEY', default='django-insecure-key')
DEBUG = True
ALLOWED_HOSTS = ['*']

# Aplicações instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'chat',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS primeiro!
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sls_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sls_backend.wsgi.application'

# PostgreSQL
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

# MongoDB config (via pymongo)
MONGO_URI = config('MONGO_URI')
MONGO_DB_NAME = config('MONGO_DB_NAME', default='chatlogs')

# Passwords
AUTH_PASSWORD_VALIDATORS = []

# Internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Arquivos estáticos
STATIC_URL = 'static/'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}

# CORS (libera o frontend em React)
CORS_ALLOW_ALL_ORIGINS = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Gemini API Key
GEMINI_API_KEY = config('GEMINI_API_KEY')
