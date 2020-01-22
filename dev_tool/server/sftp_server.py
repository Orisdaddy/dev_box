from channels.generic.websocket import WebsocketConsumer
from .handler import FileHandler
from dev_tool.paramiko_io.sftp_client import IoSftpClient
import paramiko
import json
import threading


class SftpConsumer(WebsocketConsumer):
    client_map = {}
    recv = None

    def connect(self):
        tab = self.scope['url_route']['kwargs']['tab']
        client = FileHandler(paramiko.Transport, IoSftpClient.from_transport)
        self.client_map[tab] = client
        self.accept()
        pk = tab.split('@')[0]
        res = client.connect(pk)
        # self.recv = threading.Thread(target=recv, args=(self,))
        # self.recv.start()

    def disconnect(self, code):
        tab = self.scope['url_route']['kwargs']['tab']
        client = self.client_map.pop(tab)
        client.close()

    def receive(self, text_data=None, bytes_data=None):
        tab = self.scope['url_route']['kwargs']['tab']
        client = self.client_map[tab]
        text_data = json.loads(text_data)
        mode = text_data['mode']
        if mode == 'upload_file':
            res = client.put_file(text_data)
            res = {
                'mode': 'upload_file',
                'status': res,
                'name': text_data['name']
            }
        elif mode == 'root_dir':
            listdir = client.root_dir_list()
            res = {
                'mode': 'root_dir',
                'files': listdir
            }

        elif mode == 'dir_list':
            path = text_data['path']
            listdir = client.dir_list(path)
            res = {
                'mode': 'dir_list',
                'files': listdir
            }

        elif mode == 'download':
            if text_data['type'] != 'd':
                content = client.get_file(text_data['path'])
                res = {
                    'mode': 'download',
                    'name': text_data['name'],
                    'content': content.decode('utf-8')
                }

        elif mode == 'delete':
            if text_data['type'] != 'd':
                status = client.remove(text_data['path'])
                res = {
                    'mode': 'delete',
                    'name': text_data['name'],
                    'status': status
                }
        self.send(json.dumps(res))

