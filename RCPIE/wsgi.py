"""
WSGI config for RCPIE project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RCPIE.settings')

def _run_migrations_if_requested():
	"""Run migrations at startup if RUN_MIGRATIONS_AT_STARTUP env var is set to "True".

	This is a guarded, optional workaround for platforms where release commands
	can't be run interactively. Set `RUN_MIGRATIONS_AT_STARTUP=True` in the
	environment to enable. It's safe to disable after migrations succeed.
	"""
	try:
		if os.environ.get('RUN_MIGRATIONS_AT_STARTUP', 'False') == 'True':
            import django
            from django.core.management import call_command
            import sys
            
            # Setup Django before running migrations
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RCPIE.settings')
            django.setup()
            

_run_migrations_if_requested()

application = get_wsgi_application()
