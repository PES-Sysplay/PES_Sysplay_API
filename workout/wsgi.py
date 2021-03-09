"""
WSGI config for workout project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

SETTINGS_FILE = os.environ.get('SETTINGS_FILE', 'workout.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', SETTINGS_FILE)

application = get_wsgi_application()
