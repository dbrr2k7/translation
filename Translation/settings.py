"""
Django settings for the IOI Translation project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import raven

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get('TRANS_DEBUG', '0')) > 0

PYPPETEER_PDF_OPTIONS = {
    'margin': {
        'left': '0.75in',
        'right': '0.75in',
        'top': '0.62in',
        'bottom': '1in',
    },
    'format': 'A4',
    'printBackground': True,
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'raven.contrib.django.raven_compat',
    'import_export',
    'trans',
    'print_job_queue',
]

WEBSOCKET_URL = '/ws3/'
WSGI_APPLICATION = 'ws4redis.django_runserver.application'

MIDDLEWARE = [
    'xff.middleware.XForwardedForMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Translation.urls'

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
                'django.template.context_processors.static',
                'trans.context_processors.ioi_settings',
                'trans.context_processors.ioi_user',
            ],
        },
    },
]

WSGI_APPLICATION = 'Translation.wsgi.application'
# WSGI_APPLICATION = 'ws4redis.django_runserver.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': '5432',
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://%s:%s/%s" % (os.environ['REDIS_HOST'], os.environ.get('REDIS_PORT', '6379'), os.environ['REDIS_DB']),
        'TIMEOUT': None,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_SECURE = int(os.environ.get('SESSION_COOKIE_SECURE', 1)) != 0

# RAVEN_CONFIG = {
#     'dsn': os.environ['RAVEN_DSN'],
#     # If you are using git, you can also automatically configure the
#     # release based on the git info.
#     'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
# }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'timestamped': {
            'format': '%(asctime)-15s.%(msecs)03d %(levelname)-5.5s [%(process)s] (%(name)s) %(message)s',
            'style': '%',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'formatter': 'timestamped',
        },
        'trans': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/trans.log'),
            'formatter': 'timestamped',
        },
        'print_job_queue': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/print_job_queue.log'),
            'formatter': 'timestamped',
        },
        'stderr': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': os.environ.get('LOG_HANDLERS', 'stderr').split(','), 	#show errors
#            'handlers': ['file', 'sentry'],	#not show errors
            'level': 'DEBUG',
            'propagate': True,
        },
        'trans': {
            'handlers': os.environ.get('TRANS_LOG_HANDLERS', 'stderr').split(','),
            'level': 'DEBUG',
            'propagate': True,
        },
        'print_job_queue': {
            'handlers': os.environ.get('PRINT_JOB_QUEUE_LOG_HANDLERS', 'stderr').split(','),
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.environ.get('TRANS_TIME_ZONE', 'UTC')

USE_I18N = True
USE_L10N = True
USE_TZ = True

TRANSLATION_EDIT_TIME_OUT = 120

# Should we produce one print job per team (as opposed to one per contestant)?
# The former prints faster, the latter lets the printer collate paper per contestant.
PRINT_BATCH_WHOLE_TEAM = False

# Print jobs are padded with blank pages so that each task has an even number of pages.
# Enable if you use duplex printing.
PRINT_BATCH_DUPLEX = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
CACHE_DIR = os.path.join(BASE_DIR, "cache")

HOST_URL = os.environ.get('TRANS_URL', 'http://127.0.0.1:9000/')

ALLOWED_HOSTS = ['*']
USE_X_FORWARDED_HOST = True
XFF_TRUSTED_PROXY_DEPTH = 1
XFF_STRICT = True
CSRF_TRUSTED_ORIGINS = [HOST_URL + '*']
