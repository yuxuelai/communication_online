
from django.urls import path ,re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/private/(?P<room_name>\w+)/$', PrivateChatConsumer.as_asgi()),
    re_path(r'ws/p-p/(?P<user_name>\w+)/$', PrivateChatConsumer2.as_asgi()),
    
]







