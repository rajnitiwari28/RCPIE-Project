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
			# Import here to avoid importing Django before settings configured
			from django.core.management import call_command
			import sys
			print('RUN_MIGRATIONS_AT_STARTUP=True; running migrations...', file=sys.stderr)
			call_command('migrate', '--noinput')
			print('Migrations complete.', file=sys.stderr)
	except Exception as exc:
		# Log but do not prevent the app from starting; release logs will show the error
		import traceback, sys
		print('Error running migrations at startup:', file=sys.stderr)
		traceback.print_exc()


_run_migrations_if_requested()

application = get_wsgi_application()
