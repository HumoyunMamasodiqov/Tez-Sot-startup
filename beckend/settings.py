from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# === SECURITY ===
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    'tezsotuz.onrender.com',
    '127.0.0.1',
    'localhost',
    '.onrender.com'
]

# === APPS ===
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'fronend',
    'authentication',

    # whitenoise static files
    'whitenoise.runserver_nostatic',
]

# === MIDDLEWARE ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # STATIC FILE SERVE
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'beckend.urls'

# === TEMPLATES ===
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'beckend.wsgi.application'

# === DATABASE ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# === PASSWORDS ===
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# === LANGUAGE & TIME ===
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# === STATIC FILES (Render uchun to‘liq sozlangan) ===
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Render static uchun majburiy
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# whitenoise gzip + brotli
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# === MEDIA ===
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# === OTHER ===
SECURE_BROWSER_XSS_FILTER = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
