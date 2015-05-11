#!/bin/bash

cd /var/www/antisocial/antisocial/
exec python manage.py celery worker --settings=antisocial.settings_docker
