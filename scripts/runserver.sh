#!/bin/sh
set -e 

gunicorn project.wsgi:application \
    --bind 0.0.0.0:8000\
    --workers 2 \
    --threads 2 \
    --timeout 120