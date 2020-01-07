from dev_tool.models import Services


class CommonHandler:
    def __init__(self, client):
        self.client = client

    def connect(self, pk):
        try:
            server_obj = Services.objects.filter(pk=pk).first()
            self.client.connect(
                hostname=server_obj.host,
                port=server_obj.port,
                username=server_obj.username,
                password=server_obj.password
            )
            res = {
                'mode': 'login',
                'status': 'success',
                'data': {
                    'hostname': server_obj.host,
                    'username': server_obj.username
                }
            }
            return res
        except Exception as e:
            res = {
                'mode': 'login',
                'status': 'error',
                'msg': str(e)
            }
            return res

    def push(self, common):
        _, stdout, _ = self.client.exec_command(common)
        return stdout.read().decode('utf-8')

    def close(self):
        self.client.close()
