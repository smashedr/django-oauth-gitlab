import os
from configparser import ConfigParser
from distutils.util import strtobool

settings_file = 'settings.ini'

ROOT_URLCONF = 'cstools.urls'
WSGI_APPLICATION = 'cstools.wsgi.application'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = ConfigParser()
CONFIG.read(os.path.join(BASE_DIR, settings_file))

LOGIN_URL = '/oauth/'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
LOGIN_REDIRECT_URL = '/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
TEMPLATES_DIRS = [os.path.join(BASE_DIR, 'templates')]

ALLOWED_HOSTS = CONFIG['django']['allowed_hosts'].split(' ')
DEBUG = strtobool(CONFIG['django']['debug'])
SECRET_KEY = CONFIG['django']['secret']
STATIC_ROOT = CONFIG['django']['static_root']
MEDIA_ROOT = CONFIG['django']['media_root']

LANGUAGE_CODE = CONFIG['django']['language_code']
TIME_ZONE = CONFIG['django']['time_zone']

USE_I18N = True
USE_L10N = True
USE_TZ = True

if 'sqlite_db' in CONFIG['django']:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': CONFIG['database']['name'],
            'USER': CONFIG['database']['user'],
            'PASSWORD': CONFIG['database']['pass'],
            'HOST': CONFIG['database']['host'],
            'PORT': CONFIG['database']['port'],
        }
    }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': ('%(asctime)s - %(levelname)s '
                       '%(module)s.%(funcName)s:%(lineno)d - '
                       '%(message)s')
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': CONFIG['logging']['log_file'],
            'formatter': 'standard',
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': [CONFIG['logging']['django_handler']],
            'level': CONFIG['logging']['django_level'],
            'propagate': True,
        },
        'app': {
            'handlers': [CONFIG['logging']['app_handler']],
            'level': CONFIG['logging']['app_level'],
            'propagate': True,
        },
    },
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'oauth',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATES_DIRS,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
