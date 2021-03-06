"""
Django settings for otus_django_courses project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(
    EMAIL_HOST=(str, ''),
    EMAIL_HOST_PASSWORD=(str, ''),
    EMAIL_HOST_USER=(str, ''),
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ['127.0.0.1', '85.143.173.4', 'oc.space-coding.com', '0.0.0.0', 'localhost']),
    INFLUXDB_HOST=(str, 'localhost'),
    INFLUXDB_PORT=(int, 8086),
    INFLUXDB_DB=(str, 'otus'),
    MONITORING=(bool, False),
    DB_DRIVER=(str, 'sqlite'),
    DB_NAME=(str, os.path.join(BASE_DIR, 'db.sqlite3')),
    DB_USER=(str, ''),
    DB_PASSWORD=(str, ''),
    DB_IP=(str, ''),
    DB_PORT=(str, ''),
    SENTRY_KEY=(str, ''),
    SENTRY_ID=(int, 0)
)

environ.Env.read_env()

if env('SENTRY_KEY') and env('SENTRY_ID'):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn="https://{}@sentry.io/{}".format(env('SENTRY_KEY'), env('SENTRY_ID')),
        integrations=[DjangoIntegration()]
    )

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9lslw(yc=$ae7z^h^zt)w3$e80elt0d_^=v*i5ag177t06-h_4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')
INTERNAL_IPS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    # Main
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Modules
    'debug_toolbar',
    'django_extensions',
    'rest_framework',
    'django_rq',

    # Apps
    'courses',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'otus_django_courses.middleware.ResponseTimeMiddleware'
]

ROOT_URLCONF = 'otus_django_courses.urls'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'URL_FIELD_NAME': 'href',
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'otus_django_courses.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DB_DRIVERS = {
    'postgres': 'django.db.backends.postgresql_psycopg2',
    'sqlite': 'django.db.backends.sqlite3'
}

DATABASES = {
    'default': {
        'ENGINE': DB_DRIVERS[env('DB_DRIVER')],
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_IP'),
        'PORT': env('DB_PORT'),
    }
}

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        # 'PASSWORD': 0,
        'DEFAULT_TIMEOUT': 360,
    },
    'lesson_reminder': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        # 'PASSWORD': 0,
        'DEFAULT_TIMEOUT': 360,
    },
    'lesson_reminder_test': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        # 'PASSWORD': 0,
        'DEFAULT_TIMEOUT': 360,
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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/keys

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

EMAIL_USE_TLS = True

EMAIL_PORT = 25
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')

RQ_SHOW_ADMIN_LINK = True
