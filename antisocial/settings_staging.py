# flake8: noqa
from settings_shared import *

TEMPLATE_DIRS = (
    "/var/www/antisocial/antisocial/antisocial/templates",
)

MEDIA_ROOT = '/var/www/antisocial/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/antisocial/antisocial/sitemedia'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'antisocial',
        'HOST': '',
        'PORT': 6432,
        'USER': '',
        'PASSWORD': '',
    }
}

COMPRESS_ROOT = "/var/www/antisocial/antisocial/media/"
DEBUG = False
TEMPLATE_DEBUG = DEBUG
STAGING_ENV = True

try:
    from local_settings import *
except ImportError:
    pass
