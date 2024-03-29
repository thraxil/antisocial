# flake8: noqa
from settings_shared import *

DEBUG = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "postgres",
        "USER": "postgres",
        "HOST": "db",
        "PORT": 5432,
        "ATOMIC_REQUESTS": True,
    }
}

EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
CELERY_BROKER_URL = "amqp://guest:guest@rabbitmq:5672/"
BROKER_URL = "amqp://guest:guest@rabbitmq:5672/"

try:
    from local_settings import *
except ImportError:
    pass
