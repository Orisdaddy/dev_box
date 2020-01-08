from dev_tool.models import Services


class CommonHandler:
    def __init__(self, client):
        self.client = client
        self.chan = None
        self.is_root = False

    def connect(self, pk):
        try:
            server_obj = Services.objects.filter(pk=pk).first()
            self.client.connect(
                hostname=server_obj.host,
                port=server_obj.port,
                username=server_obj.username,
                password=server_obj.password
            )
            if server_obj.username == 'root':
                self.is_root = True
            self.chan = self.client.invoke_shell()
            res = {
                'mode': 'login',
                'status': 'success',
                'data': {
                    'hostname': server_obj.host,
                    'username': server_obj.username,
                }
            }
            return res, self.chan
        except Exception as e:
            res = {
                'mode': 'login',
                'status': 'error',
                'msg': str(e)
            }
            return res

    def push(self, common):
        self.chan.send(common + '\r')

    def close(self):
        self.client.close()



