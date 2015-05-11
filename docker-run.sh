#!/bin/bash

cd /var/www/antisocial/antisocial/
python manage.py migrate --noinput --settings=antisocial.settings_docker
python manage.py collectstatic --noinput --settings=antisocial.settings_docker
python manage.py compress --settings=antisocial.settings_docker
exec gunicorn --env \
  DJANGO_SETTINGS_MODULE=antisocial.settings_docker \
  antisocial.wsgi:application -b 0.0.0.0:8000 -w 3 \
  --access-logfile=- --error-logfile=-
