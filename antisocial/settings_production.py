# flake8: noqa
from settings_shared import *
import os.path

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
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
        'ATOMIC_REQUESTS': True,
    }
}

COMPRESS_ROOT = os.path.join(os.path.dirname(__file__), "../media")
DEBUG = False
TEMPLATE_DEBUG = DEBUG
COMPRESS_OFFLINE = True

STATICFILES_DIRS = ()
STATIC_ROOT = "/var/www/antisocial/antisocial/media/"

if 'migrate' not in sys.argv:
    INSTALLED_APPS = INSTALLED_APPS + [
        'raven.contrib.django.raven_compat',
    ]

try:
    from local_settings import *
except ImportError:
    pass
