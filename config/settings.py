import os
from pathlib import Path
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Prefer Vercel CLI's local environment file; process environment variables still take precedence.
load_dotenv(BASE_DIR / '.env.local')
load_dotenv(BASE_DIR / '.env')

IS_VERCEL = 'VERCEL' in os.environ or os.getenv('SERVERLESS') == '1'

SECRET_KEY = os.getenv('SECRET_KEY')
if IS_VERCEL and not SECRET_KEY:
    raise ImproperlyConfigured('Set SECRET_KEY in the Vercel project environment variables.')
SECRET_KEY = SECRET_KEY or 'django-insecure-sih-yatra-ai-key-prototype-2026'

DEBUG = os.getenv('DEBUG', 'False' if IS_VERCEL else 'True').lower() in ('true', '1', 't')

ALLOWED_HOSTS = os.getenv(
    'ALLOWED_HOSTS',
    'localhost,127.0.0.1,.vercel.app,.now.sh',
).split(',')
ALLOWED_HOSTS.extend(['.vercel.app', '.now.sh', 'localhost', '127.0.0.1'])
ALLOWED_HOSTS = list(set([h.strip() for h in ALLOWED_HOSTS if h.strip()]))

CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'https://*.now.sh',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
extra_csrf = os.getenv('CSRF_TRUSTED_ORIGINS', '')
if extra_csrf:
    CSRF_TRUSTED_ORIGINS.extend([origin.strip() for origin in extra_csrf.split(',') if origin.strip()])

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'tourism',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'frontend' / 'dist', BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Use persistent PostgreSQL on Vercel and local SQLite for development.
if os.getenv('DATABASE_URL'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=IS_VERCEL,
        )
    }
elif IS_VERCEL:
    raise ImproperlyConfigured('Set DATABASE_URL to a persistent PostgreSQL database in Vercel.')
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'frontend' / 'dist',
    BASE_DIR / 'static',
]
STATIC_ROOT = Path('/tmp/staticfiles') if IS_VERCEL else (BASE_DIR / 'staticfiles')

# WhiteNoise Configuration for Vercel & Production Static File Serving
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'my_trips'
LOGOUT_REDIRECT_URL = 'home'

# AI Integration settings
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '') or os.getenv('AI_API_KEY', '')
AI_API_KEY = GEMINI_API_KEY
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-3.6-flash')

