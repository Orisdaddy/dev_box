from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import paramiko


class MachineShellConsumer(WebsocketConsumer):
    client_map = {}

    def connect(self):
        tab = self.scope['url_route']['kwargs']['tab']
        client = paramiko.SSHClient()
        self.client_map[tab] = client

    def disconnect(self, code):
        tab = self.scope['url_route']['kwargs']['tab']
        client = self.client_map.pop(tab)
        client.close()

    def receive(self, text_data=None, bytes_data=None):
        pass
