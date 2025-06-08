"""
ASGI config for nuSeqQuery project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""


import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application;
import django
django.setup()
import api.routing;

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nuSeqQuery.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        api.routing.websocket_urlpatterns   
    ),
})
