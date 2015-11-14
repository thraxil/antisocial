#!/bin/bash

cd /var/www/$APP/$APP/

export DJANGO_SETTINGS_MODULE="$APP.settings_docker"

if [ "$1" == "migrate" ]; then
		exec python manage.py migrate --noinput
fi

if [ "$1" == "collectstatic" ]; then
		exec python manage.py collectstatic --noinput
fi

if [ "$1" == "compress" ]; then
		exec python manage.py compress
fi

if [ "$1" == "shell" ]; then
		exec python manage.py shell
fi

if [ "$1" == "worker" ]; then
		exec python manage.py celery worker
fi

if [ "$1" == "beat" ]; then
		exec python manage.py celery beat
fi

# run arbitrary commands
if [ "$1" == "manage" ]; then
		shift
		exec python manage.py "$@"
fi


if [ "$1" == "run" ]; then
		exec gunicorn --env \
				 DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE \
				 $APP.wsgi:application -b 0.0.0.0:8000 -w 3 \
				 --access-logfile=- --error-logfile=-
fi
