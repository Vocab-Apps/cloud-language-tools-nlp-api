#!/bin/sh
WORKERS="${GUNICORN_WORKERS:-1}" 
echo "starting gunicorn with ${WORKERS} workers" 
exec gunicorn --workers $WORKERS -b :8042 --timeout 120 --access-logfile - --error-logfile - api:app