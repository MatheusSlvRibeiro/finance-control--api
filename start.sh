#!/bin/bash
set -e

export DJANGO_SETTINGS_MODULE=backend.settings.production

echo "=== Settings: $DJANGO_SETTINGS_MODULE ==="
echo "=== Database URL: ${DATABASE_URL:0:40}... ==="

echo "=== Running migrations ==="
python manage.py migrate --noinput

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput --clear

echo "=== Starting Gunicorn ==="
exec gunicorn backend.wsgi:application \
  --bind 0.0.0.0:${PORT:-8000} \
  --workers 2 \
  --timeout 120 \
  --log-level info \
  --access-logfile -
