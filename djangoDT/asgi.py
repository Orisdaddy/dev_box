"""
ASGI config for djangoDT project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from djangoDT import routing
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoDT.settings')

# application = get_wsgi_application()
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(URLRouter(
        routing.websocket_urlpatterns
    ))
})
