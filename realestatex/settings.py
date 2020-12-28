"""
Django settings for realestatex project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from .config import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['test.swiftliving.us']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.gis',
    'rest_framework',
    'phonenumber_field',
    'bootstrap3',
    'users',
    'property.apps.PropertyConfig',
    'students',
    'services',
    'checkout',
    'notifications',
    'channels',
    'chat',
    'discussion',
    'storages',
    'defender',
    'captcha',
    'resources',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'defender.middleware.FailedLoginMiddleware',
]

ROOT_URLCONF = 'realestatex.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],
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

WSGI_APPLICATION = 'realestatex.wsgi.application'
ASGI_APPLICATION = 'realestatex.routing.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
   'default' : {
       'ENGINE' : 'django.contrib.gis.db.backends.postgis',
    #    'ENGINE' : 'django.db.backends.postgresql',
       'NAME' : DB_NAME,
       'USER' : DB_USER,
       'PASSWORD' : DB_PASSWORD,
       "HOST": DB_HOST,
       "PORT": DB_PORT
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# PHONENUMBER_DB_FORMAT = 'INTERNATIONAL'

# PHONENUMBER_DEFAULT_REGION = 'US'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, 'static'),
#)


#MEDIA FILES


MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


#LOGIN AND LOGOUT GOBAL CONFIG


LOGIN_URL = "/"

# LOGIN_REDIRECT_URL = "dashboard/"

LOGOUT_REDIRECT_URL = "/"


#SESSION RELATED SETTINGS


SESSION_EXPIRE_AT_BROWSER_CLOSE = True

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True


#GOOGLE KEY FOR PLACES


GOOGLE_MAPS_API_KEY = GOOGLE_API_KEY


#AWS CONFIGS


AWS_ACCESS_KEY_ID = AWS_API_KEY

AWS_SECRET_ACCESS_KEY = AWS_API_SECRET_ACCESS_KEY

AWS_STORAGE_BUCKET_NAME = AWS_BUCKET_NAME

AWS_S3_FILE_OVERWRITE = False

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


#TWILIO CONFIGS


TWILIO_ACCOUNT_SID = TWILIO_ACCOUNT_SID_KEY
TWILIO_AUTH_TOKEN = TWILIO_AUTH_TOKEN_KEY
TWILIO_VERIFICATION_SID = TWILIO_VERIFICATION_SID_KEY


#RECAPTCHA CONFIGS

#DEFAULT V2 CHECKBOX KEYS
RECAPTCHA_PUBLIC_KEY = RECAPTCHA_PUBLIC_KEY_API
RECAPTCHA_PRIVATE_KEY = RECAPTCHA_PRIVATE_KEY_API

#V3 KEYS
RECAPTCHA_V3_PUBLIC_KEY = RECAPTCHA_V3_PUBLIC_KEY_API
RECAPTCHA_V3_PRIVATE_KEY = RECAPTCHA_V3_PRIVATE_KEY_API
RECAPTCHA_REQUIRED_SCORE = 0.8

#DEFENDER SETTINGS

DEFENDER_LOGIN_FAILURE_LIMIT = 2

# DEFENDER_LOGIN_FAILURE_LIMIT_IP = 10

# DEFENDER_COOLOFF_TIME = 10

DEFENDER_LOCKOUT_TEMPLATE = 'users/defenderLockout.html'

DEFENDER_ACCESS_ATTEMPT_EXPIRATION = 2*24

# DEFENDER_LOCKOUT_URL = '/'

# DEFENDER_REDIS_URL = default redis://localhost:6379/0 example redis://:mypassword@localhost:6379/0)
