#!/bin/bash
set -e


echo "Waiting for database..."
sleep 10


echo "Applying migrations..."
python manage.py migrate --noinput


echo "Collecting static files..."
python manage.py collectstatic --noinput


echo "Starting Apache..."
apache2ctl -D FOREGROUND