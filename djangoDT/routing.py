from django.urls import re_path
from dev_tool.views.server import server

websocket_urlpatterns = [
    re_path('ws/server/(?P<host>[^/]+)/', server.MachineShellConsumer),
]
