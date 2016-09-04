# Django settings for antisocial project.
import os.path
import djcelery

from thraxilsettings.shared import common

base = os.path.dirname(__file__)
locals().update(common(app='antisocial', base=base))

# extended common settings. remember to '# noqa' them.

ALLOWED_HOSTS += ['.thraxil.org']  # noqa

INSTALLED_APPS += [  # noqa
    'userena',
    'guardian',
    'easy_thumbnails',
    'bootstrapform',
    'djcelery',

    'antisocial.main',
    'antisocial.profile',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.dirname(__file__), "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
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

djcelery.setup_loader()
