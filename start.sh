#!/bin/bash
set -eoux pipefail

WORKERS="${GUNICORN_WORKERS:-1}" 
GUNICORN_THREADS="${GUNICORN_THREADS:-8}"
MAX_REQUESTS="${GUNICORN_MAX_REQUESTS:-1000}"
MAX_REQUESTS_JITTER="${GUNICORN_MAX_REQUESTS_JITTER:-100}"
echo "starting gunicorn with ${WORKERS} workers, ${GUNICORN_THREADS} threads, and ${MAX_REQUESTS} max requests, max requests jitter ${MAX_REQUESTS_JITTER}" 
exec gunicorn --workers $WORKERS --threads ${GUNICORN_THREADS} -b :8042 --timeout 120 --max-requests ${MAX_REQUESTS} --max-requests-jitter ${MAX_REQUESTS_JITTER} --access-logfile - --error-logfile - api:app