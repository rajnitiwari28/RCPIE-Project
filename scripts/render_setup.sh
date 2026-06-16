#!/usr/bin/env bash
set -euo pipefail

export DJANGO_SETTINGS_MODULE=RCPIE.settings

echo "=== Render release: debug start ==="
echo "User: $(whoami || true)"
echo "Python: $(python --version 2>&1 || true)"
echo "Which python: $(command -v python || true)"
echo "VENV: ${VIRTUAL_ENV:-<none>}"
echo "DATABASE_URL present: ${DATABASE_URL:-<not set>}"
echo "DJANGO_SETTINGS_MODULE: ${DJANGO_SETTINGS_MODULE:-RCPIE.settings}"

echo "Pip packages (top):"
python -m pip show psycopg2-binary || true
python -m pip freeze | sed -n '1,80p' || true

echo "Running render setup: migrate, collectstatic, create superuser if provided"

if [ -n "${DATABASE_URL:-}" ]; then
  echo "DATABASE_URL is set (will use Postgres)"
else
  echo "DATABASE_URL is not set — using SQLite, which is ephemeral on Render"
fi

python - <<'PY'
from django.conf import settings
print('DB engine:', settings.DATABASES['default'].get('ENGINE'))
print('DB NAME:', settings.DATABASES['default'].get('NAME'))
PY

echo "Applying migrations..."
if ! python manage.py migrate --noinput; then
  echo "ERROR: migrate failed"
  echo "Showing auth migrations and current migration list..."
  python manage.py showmigrations auth || true
  python manage.py showmigrations RCPIEAPP || true
  exit 1
fi

echo "Migrations applied successfully"

echo "Showing auth migration status..."
python manage.py showmigrations auth || true

echo "Collecting static files..."
python manage.py collectstatic --noinput || true

if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && [ -n "${DJANGO_SUPERUSER_EMAIL:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
  echo "Ensuring superuser ${DJANGO_SUPERUSER_USERNAME} exists..."
  python - <<'PY'
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RCPIE.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
if username and password:
    u = User.objects.filter(username=username).first()
    if not u:
        User.objects.create_superuser(username=username, email=email or '', password=password)
        print('Superuser created')
    else:
        u.set_password(password)
        u.is_staff = True
        u.is_superuser = True
        u.save()
        print('Superuser updated')
else:
    print('Superuser env vars missing')
PY
else
  echo "DJANGO_SUPERUSER_* env vars not provided; skipping superuser creation"
fi

echo "=== Render release: debug end ==="
