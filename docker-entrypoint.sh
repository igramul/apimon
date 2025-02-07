#!/bin/sh

exec /venv/bin/gunicorn -b :5000 --access-logfile - --error-logfile - flaskapp:app
