#!/usr/bin/env bash
set -euo pipefail

echo "Running render setup: migrate, collectstatic, create superuser if provided"

# Apply migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Create or ensure superuser if environment vars are present
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

echo "Render setup complete"
