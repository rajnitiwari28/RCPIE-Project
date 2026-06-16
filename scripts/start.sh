#!/usr/bin/env bash
set -euo pipefail

echo "=== Render start: running migrations before launching gunicorn ==="
if [ -n "${DATABASE_URL:-}" ]; then
  echo "DATABASE_URL is set"
else
  echo "DATABASE_URL is not set; using SQLite (not recommended for Render)"
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput || true

exec gunicorn RCPIE.wsgi --bind 0.0.0.0:$PORT
