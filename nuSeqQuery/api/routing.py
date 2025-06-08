from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/sequence/', consumers.SeqConsumer.as_asgi()),
]