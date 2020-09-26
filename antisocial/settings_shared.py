# Django settings for antisocial project.
import os.path

from thraxilsettings.shared import common

base = os.path.dirname(__file__)
locals().update(common(app='antisocial', base=base))

# extended common settings. remember to '# noqa' them.

ALLOWED_HOSTS += ['.thraxil.org', '127.0.0.1']  # noqa

INSTALLED_APPS += [  # noqa
    'bootstrap3',
    'bootstrapform',

    'antisocial.main',
]

MIDDLEWARE += [  # noqa
    'beeline.middleware.django.HoneyMiddleware',
]

# project specific settings

PROJECT_APPS = [
    'antisocial.main',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

ANONYMOUS_USER_ID = -1

LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'

BROKER_URL = "amqp://guest:guest@localhost:5672//"
CELERYD_CONCURRENCY = 4

GZIP_CONTENT_TYPES = (
    'text/css',
    'application/javascript',
    'application/x-javascript',
    'text/javascript'
)
COMPRESS_STORAGE = 'compressor.storage.GzipCompressorFileStorage'
AWS_IS_GZIPPED = True
AWS_DEFAULT_ACL = 'public-read'

# default off
HONEYCOMB_WRITEKEY = None
HONEYCOMB_DATASET = None
