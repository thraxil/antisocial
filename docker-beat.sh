#!/bin/bash

cd /var/www/antisocial/antisocial/
exec python manage.py celery beat --settings=antisocial.settings_docker
