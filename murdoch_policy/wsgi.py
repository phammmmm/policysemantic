"""
WSGI config for murdoch_policy project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
#from murdoch_policy.wsgi import murdochpolicyapp

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'murdoch_policy.settings')

application = get_wsgi_application()
#application = murdochpolicyapp(application)
