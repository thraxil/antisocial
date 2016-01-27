# flake8: noqa
from settings_shared import *
from thraxilsettings.docker import common
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
    ))
OPBEAT_ORGANIZATION_ID=os.environ.get('OPBEAT_ORGANIZATION_ID')
OPBEAT_APP_ID=os.environ.get('OPBEAT_APP_ID')
OPBEAT_SECRET_TOKEN=os.environ.get('OPBEAT_SECRET_TOKEN')
if OPBEAT_ORGANIZATION_ID:
    INSTALLED_APPS += [
        'opbeat.contrib.django',
    ]
    OPBEAT = {
        'ORGANIZATION_ID': OPBEAT_ORGANIZATION_ID,
        'APP_ID': OPBEAT_APP_ID,
        'SECRET_TOKEN': OPBEAT_SECRET_TOKEN,
    }
    MIDDLEWARE_CLASSES.insert(0, 'opbeat.contrib.django.middleware.OpbeatAPMMiddleware')
