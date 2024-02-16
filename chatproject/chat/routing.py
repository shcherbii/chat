from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/<str:chat_id>/',consumers.ChatConsumer.as_asgi()),
    path("ws/", consumers.NotificationConsumer.as_asgi()),
]