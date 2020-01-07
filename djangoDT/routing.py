from django.urls import re_path
from dev_tool.server import server

websocket_urlpatterns = [
    re_path('^ws/server/(?P<tab>.*)', server.MachineShellConsumer),
]
