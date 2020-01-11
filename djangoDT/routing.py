from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from dev_tool.server import server


websocket_urlpatterns = [
    re_path('^ws/server/(?P<tab>.*)', server.MachineShellConsumer),
]


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(URLRouter(
        websocket_urlpatterns
    ))
})


