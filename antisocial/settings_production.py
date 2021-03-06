# flake8: noqa
from .settings_shared import *
from thraxilsettings.production import common
import os.path

app = 'antisocial'
base = os.path.dirname(__file__)
cloudfront = "d115djs1mf98us.cloudfront.net"

locals().update(
    common(
        app=app,
        base=base,
        cloudfront=cloudfront,
        INSTALLED_APPS=INSTALLED_APPS,
        STATIC_ROOT=STATIC_ROOT,
    ))

try:
    from local_settings import *
except ImportError:
    pass
