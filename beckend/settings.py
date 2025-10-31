from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# === Xavfsizlik ===
SECRET_KEY = 'django-insecure-&*0@&h#k5ut#s(!r-2gbjs&&1y_)k%pch(6o(7%v*7qj*0m5@*'

DEBUG = False  # SERVERDA FALSE BO'LADI
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'tezsotuz.onrender.com', '.onrender.com']

# === Apps ===
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'fronend',
    'authentication',
]

# === Middleware ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # STATIC FAYLLAR UCHUN WHITENOISE
    'whitenoise.middleware.WhiteNoiseMiddleware',

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
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'beckend.wsgi.application'

# === Database ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# === Static ===
STATIC_URL = '/static/'

# LOCAL VA SERVERDA HAM ISHLAYDIGAN MINIMAL KONFIG
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] 

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# === Media ===
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# === Boshqa ===
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SECURE_BROWSER_XSS_FILTER = True
