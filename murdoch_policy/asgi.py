"""
ASGI config for murdoch_policy project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'murdoch_policy.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

application = get_asgi_application()
