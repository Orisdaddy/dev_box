from dev_tool.models import Services
import base64


class CommonHandler:
    def __init__(self, client):
        self.client = client
        self.chan = None

    def connect(self, pk):
        try:
            server_obj = Services.objects.filter(pk=pk).first()
            self.client.connect(
                hostname=server_obj.host,
                port=server_obj.port,
                username=server_obj.username,
                password=server_obj.password
            )
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
            return res, None

    def push(self, common):
        self.chan.send(common + '\r')

    def close(self):
        self.client.close()


FILE_TYPE_MAP = {
    'd': 0,
    '-': 1
}


class FileHandler:
    def __init__(self, transport, from_transport):
        self.transport = transport
        self.from_transport = from_transport
        self.client = None

    def connect(self, pk):
        server_obj = Services.objects.filter(pk=pk).first()
        self.transport = self.transport((server_obj.host, server_obj.port))
        self.transport.connect(
            username=server_obj.username,
            password=server_obj.password
        )
        self.client = self.from_transport(self.transport)

    def get_dir(self):
        pass

    def get_file(self, path):
        return base64.b64encode(self.client.get(path))

    def put_dir(self):
        pass

    def put_file(self, data):
        try:
            content = base64.b64decode(data['content'])
            self.client.put(content, data['size'], data['path'])
        except:
            return False
        else:
            return True

    def root_dir_list(self):
        listdir = self.client.listdir('/')
        listdir_attr = self.client.listdir_attr('/')
        for i, f in enumerate(listdir):
            stat = str(listdir_attr[i])
            if not stat.startswith('d'):
                listdir.remove(f)
        return listdir

    def dir_list(self, path):
        res = []
        listdir = self.client.listdir(path)
        listdir_attr = self.client.listdir_attr(path)
        for i, f in enumerate(listdir):
            # stat = self.client.stat('%s/%s' % (path, f))
            stat = listdir_attr[i]
            file_type = str(stat)[0]
            size = ''
            if file_type == '-':
                size = str(stat.st_size)
            res.append({
                'type': file_type,
                'size': size,
                'name': f
            })
        res.sort(key=lambda x: FILE_TYPE_MAP.get(x['type'], 2))
        return res

    def remove(self, path):
        try:
            self.client.remove(path)
        except:
            return False
        else:
            return True

    def mkdir(self):
        pass

    def close(self):
        self.transport.close()
