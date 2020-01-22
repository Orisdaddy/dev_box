from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from dev_tool.server import ssh_server, sftp_server


websocket_urlpatterns = [
    re_path('^ws/ssh_server/(?P<tab>.*)', ssh_server.MachineShellConsumer),
    re_path('^ws/sftp_server/(?P<tab>.*)', sftp_server.SftpConsumer),
]


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(URLRouter(
        websocket_urlpatterns
    ))
})


