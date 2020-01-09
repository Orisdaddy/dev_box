from .database import build_db
import subprocess


def start():
    command = 'pip3 install -r ../../requirement/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/'
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    for line in iter(p.stdout.readline, b''):
        print(line.decode())
    p.stdout.close()
    p.wait()
    print('构建数据库中..')
    build_db()
