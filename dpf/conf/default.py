from datetime import date
import os


JINGO_EXCLUDE_APPS = ('admin', )


#
# Project logic
#

SERVE_FILES = False
DEBUG = False


#
# Database settings
#

DATABASES = {
    'default': {'NAME': 'dpf2014',
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'USER': '',
                'PASSWORD': '',
                'HOST': ''},
}


#
# Django settings
#

ALLOWED_HOSTS = ('*', )

WSGI_APPLICATION = 'dpf.wsgi.application'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

INTERNAL_IPS = ('127.0.0.1', )

# administration and email
ADMINS = (('Dev', 'dev@pitchfork.com'), )
MANAGERS = ADMINS
DEFAULT_FROM_EMAIL = 'dpf-error-bot@pitchfork.com'
EMAIL_SUBJECT_PREFIX = '[dpf] '

# secret key for encrypting user passwords
SECRET_KEY = '$!svma^61b+=ybma(!=)3ns1^!ysy2tyd=lic=t5%fc^0%a%4='

# admin media url
ADMIN_MEDIA_PREFIX = '/static/admin/'

# which apps are installed
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.redirects',

    'gunicorn',
    'jingo',

    'dpf',
    'projections',
)


#
# Templating
#

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
)

# enable jingo by default
TEMPLATE_LOADERS = (
    'jingo.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


#
# Using S3 for storage
#

# custom storage backend (s3/cloudfront)
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# AWS_ACCESS_KEY_ID = ''
# AWS_SECRET_ACCESS_KEY = ''
# AWS_STORAGE_BUCKET_NAME = 'dpf-cdn'
# AWS_S3_SECURE_URLS = False
# AWS_QUERYSTRING_AUTH = False
# AWS_S3_FILE_OVERWRITE = True
# AWS_IS_GZIPPED = True
# AWS_HEADERS = {'Expires': 'Thu, 15 Apr %s 20:00:00 GMT' % (date.today().year + 10),
#                'Cache-Control': 'max-age=86400'}

SITE_ID = 1

DATABASE_OPTIONS = {'init_command': 'SET storage_engine=INNODB',
                    'use_unicode': True,
                    'charset': 'utf8'}


#
# Localization
#

# local development timezone
TIME_ZONE = 'America/Chicago'

# this is DISABLED, as all time is stored and displayed in
# absolute America/Chicago time. this can be enabled once
# we've ensured that all storage changes are correctly
# reflected on the site.
USE_TZ = False

# language code for this installation.
USE_I18N = False
USE_L10N = False
LANGUAGE_CODE = 'en-us'

# default date formats
DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%I:%S'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
DATETIME_INPUT_FORMATS = [
    '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d',
    '%m/%d/%Y %H:%M:%S', '%m/%d/%Y %H:%M', '%m/%d/%Y',
    '%m/%d/%y %H:%M:%S', '%m/%d/%y %H:%M', '%m/%d/%y',
    '%Y-%m-%d %I:%M:%p', '%m/%d/%Y %I:%M:%p',
    '%m/%d/%y %I:%M:%p',
]

ROOT_URLCONF = 'dpf.urls.default'


#
# Basic path settings
#

PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../'))

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/')

MEDIA_URL = "/media/"

TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, 'templates/'), )


#
# Staticfiles settings
#

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'public/')
STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'static/'), )

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


#
# Logging
#

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
