# flake8: noqa
from .settings_shared import *
from thraxilsettings.docker import common
import os
import os.path

app = 'antisocial'
base = os.path.dirname(__file__)

locals().update(
    common(
        app=app,
        base=base,
        celery=True,
        INSTALLED_APPS=INSTALLED_APPS,
        STATIC_ROOT=STATIC_ROOT,
        MIDDLEWARE=MIDDLEWARE,
    ))

CELERY_BROKER_URL = os.environ['BROKER_URL']
BROKER_URL = os.environ['BROKER_URL']

RAVEN_DSN = os.environ.get('RAVEN_DSN', None)

if RAVEN_DSN:
    RAVEN_CONFIG = {
        'dsn': RAVEN_DSN,
    }
