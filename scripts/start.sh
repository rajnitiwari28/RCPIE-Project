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

if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && [ -n "${DJANGO_SUPERUSER_EMAIL:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
  echo "Ensuring superuser ${DJANGO_SUPERUSER_USERNAME} exists..."
  python - <<'PY'
import os
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

exec gunicorn RCPIE.wsgi --bind 0.0.0.0:$PORT
