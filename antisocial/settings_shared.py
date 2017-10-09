# Django settings for antisocial project.
import os.path

from thraxilsettings.shared import common

base = os.path.dirname(__file__)
locals().update(common(app='antisocial', base=base))

# extended common settings. remember to '# noqa' them.

ALLOWED_HOSTS += ['.thraxil.org']  # noqa

INSTALLED_APPS += [  # noqa
    'userena',
    'guardian',
    'easy_thumbnails',
    'bootstrap3',
    'bootstrapform',

    'antisocial.main',
    'antisocial.profile',
]

# project specific settings

PROJECT_APPS = [
    'antisocial.main',
]

AUTHENTICATION_BACKENDS = [
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
]

ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'profile.Profile'

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
