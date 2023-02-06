# flake8: noqa
import os
import os.path

from .settings_shared import *  # isort:skip
from thraxilsettings.docker import common  # isort:skip


app = "antisocial"
base = os.path.dirname(__file__)

locals().update(
    common(
        app=app,
        base=base,
        celery=True,
        INSTALLED_APPS=INSTALLED_APPS,
        STATIC_ROOT=STATIC_ROOT,
        MIDDLEWARE=MIDDLEWARE,
    )
)

CELERY_BROKER_URL = os.environ["BROKER_URL"]
BROKER_URL = os.environ["BROKER_URL"]

HONEYCOMB_WRITEKEY = os.environ.get("HONEYCOMB_WRITEKEY")
HONEYCOMB_DATASET = os.environ.get("HONEYCOMB_DATASET")
