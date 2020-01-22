from channels.generic.websocket import WebsocketConsumer
from .handler import CommonHandler
import paramiko
import json
import threading

import inspect
import ctypes
import re


def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


class MachineShellConsumer(WebsocketConsumer):
    client_map = {}
    recv = None

    def connect(self):
        tab = self.scope['url_route']['kwargs']['tab']
        cli = paramiko.SSHClient()
        client = CommonHandler(cli)
        cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client_map[tab] = client
        self.accept()
        pk = tab.split('@')[0]
        res, chan = client.connect(pk)
        self.recv = threading.Thread(target=recv, args=(chan, self))
        self.recv.start()

    def disconnect(self, code):
        tab = self.scope['url_route']['kwargs']['tab']
        client = self.client_map.pop(tab)
        if self.recv:
            stop_thread(self.recv)
        client.close()

    def receive(self, text_data=None, bytes_data=None):
        tab = self.scope['url_route']['kwargs']['tab']
        client = self.client_map[tab]
        text_data = json.loads(text_data)
        mode = text_data['mode']
        if mode == 'common':
            if re.findall('^( )*su( )*$', text_data['data']):
                res = {
                    'mode': 'other',
                    'msg': '请开启新会话切换用户'
                }
                self.send(json.dumps(res))
            client.push(text_data['data'])


def recv(chan, ws):
    while True:
        res = chan.recv(65535)
        result = {
            'mode': 'common',
            'msg': res.decode('utf-8')
        }
        ws.send(json.dumps(result))
