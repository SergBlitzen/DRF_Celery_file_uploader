#!/bin/sh

python manage.py migrate

python manage.py collectstatic

cp -r /app/collected_static/. /backend_static/static/

gunicorn --bind 0.0.0.0:8000 file_uploader.wsgi