from django.urls import re_path
from chat import consumers

websocket_urlpatterns = [
    re_path(r'^ws/room/(?P<room_id>\d+)/messages/$', consumers.ChatConsumer.as_asgi()),
]