from channels.generic.websocket import WebsocketConsumer
from .handler import CommonHandler
import paramiko
import json


class MachineShellConsumer(WebsocketConsumer):
    client_map = {}

    def connect(self):
        tab = self.scope['url_route']['kwargs']['tab']
        cli = paramiko.SSHClient()
        client = CommonHandler(cli)
        cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client_map[tab] = client
        self.accept()
        pk = tab.split('@')[0]
        res = client.connect(pk)
        self.send(json.dumps(res))

    def disconnect(self, code):
        tab = self.scope['url_route']['kwargs']['tab']
        client = self.client_map.pop(tab)
        client.close()

    def receive(self, text_data=None, bytes_data=None):
        tab = self.scope['url_route']['kwargs']['tab']
        client = self.client_map[tab]
        text_data = json.loads(text_data)
        mode = text_data['mode']
        if mode == 'login':
            res = client.connect(text_data['data'])
            self.send(json.dumps(res))
        elif mode == 'common':
            res = client.push(text_data['data'])
            res = {
                'mode': 'common',
                'data': res
            }
            res = json.dumps(res).replace(r'\n', r'\r\n')
            self.send(res)
