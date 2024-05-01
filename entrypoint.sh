#!/bin/sh

# Apply database migrations
python manage.py migrate --no-input

# Collect static files
python manage.py collectstatic --no-input

# Start Gunicorn with SSL/TLS support
gunicorn \
    --bind 0.0.0.0:8001 \
    --workers 4 \
    --timeout 120 \
    --graceful-timeout 30 \
    --keep-alive 5 \
    --preload \
    core.wsgi:application