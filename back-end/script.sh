#!/bin/bash

# Start Redis server in the background
redis-server --daemonize yes

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations models_only
python manage.py migrate

echo "Starting server..."
# celery -A firma_v02 worker --loglevel=info --detach
echo 'celery worker process started .....'
exec python manage.py runserver 0.0.0.0:8000

# celery -A firma_v02 beat --loglevel=info
