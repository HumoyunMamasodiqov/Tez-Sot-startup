"""
Django settings for beckend project.
"""

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# === Asosiy xavfsizlik ===
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-&*0@&h#k5ut#s(!r-2gbjs&&1y_)k%pch(6o(7%v*7qj*0m5@*')

# PRODUCTIONDA FALSE - Renderda False bo'lishi kerak
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Render uchun allowed hosts
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
ALLOWED_HOSTS = ['tezsot-x2zv.onrender.com', 'localhost', '127.0.0.1']
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# === Dasturlar ===
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Mening applarim - PAPKA NOMINI TEKSHIRIB QO'YING!
    'fronend',      # Agar papka nomi "fronend" bo'lsa
    'authentication', # Agar papka nomi "authentication" bo'lsa
]

# === Middleware ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Whitenoise middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'beckend.urls'

# === Templates ===
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'beckend.wsgi.application'

# === Ma'lumotlar bazasi ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Agar Renderda PostgreSQL bo'lsa
database_url = os.environ.get('DATABASE_URL')
if database_url:
    DATABASES['default'] = dj_database_url.parse(database_url)

# === Parol tekshiruvi ===
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

# === Til va vaqt ===
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# === STATIC SOZLAMALARI ===
STATIC_URL = '/static/'

# Development uchun static fayllar joylashuvi
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Production uchun static fayllar yig'iladigan papka
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise sozlamalari
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# === MEDIA ===
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# === Avtomatik ID ===
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# === Qo'shimcha xavfsizlik sozlamalari ===
if not DEBUG:
    # Xavfsizlik sozlamalari
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 yil
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True