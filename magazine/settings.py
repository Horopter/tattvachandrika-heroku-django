"""
Django settings for magazine project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import mongoengine
import logging
import django_heroku
import dj_database_url
import pymongo
import ssl

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7%4-(2pb7y(cz4#2c503%2i1wo!d$7^*otgiw2afj&jxo7wlte'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: Only for Heroku, DO NOT USE IN ACTUAL PRODUCTION
ALLOWED_HOSTS = ['*'] 


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'api',
    'drf_yasg',
    'corsheaders',
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'magazine.urls'

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

WSGI_APPLICATION = 'magazine.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# MongoDB configuration
MONGOENGINE_USER = os.getenv('MONGOENGINE_USER', 'tattvachandrika_admin')
MONGOENGINE_PASSWORD = os.getenv('MONGOENGINE_PASSWORD', 'v%21%24%23w%40k%243n%40')
MONGOENGINE_DATABASE_NAME = os.getenv('MONGOENGINE_DATABASE_NAME', 'tattvachandrika')
MONGOENGINE_HOST = os.getenv('MONGOENGINE_HOST', 'narayana.6vte2.mongodb.net')

# Updated connection string with tls=true for MongoDB Atlas
MONGOENGINE_CONNECTION_STRING = (
    f"mongodb+srv://{MONGOENGINE_USER}:{MONGOENGINE_PASSWORD}@{MONGOENGINE_HOST}/"
    f"{MONGOENGINE_DATABASE_NAME}?retryWrites=true&w=majority&tls=true"
)

DATABASE_URL = MONGOENGINE_CONNECTION_STRING

# Establish the MongoEngine default connection with updated TLS configuration
mongoengine.connect(
    MONGOENGINE_DATABASE_NAME,
    host=MONGOENGINE_CONNECTION_STRING,
)

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Try to connect using pymongo with increased timeouts and TLS enabled
try:
    mongo_client = pymongo.MongoClient(
        MONGOENGINE_CONNECTION_STRING,
        tls=True,  # Enable TLS/SSL
        tlsAllowInvalidCertificates=False,  # Ensure certificates are valid
        serverSelectionTimeoutMS=30000,  # Increase to 30 seconds
        socketTimeoutMS=30000  # Increase to 30 seconds
    )
    logger.debug('MongoDB connection successful')
except Exception as e:
    logger.error(f'Error connecting to MongoDB: {e}')


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
django_heroku.settings(locals())

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configure Django REST framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

# settings.py

CORS_ALLOW_ALL_ORIGINS = True
