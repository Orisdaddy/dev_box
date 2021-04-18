import subprocess
import os


def start():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoDT.settings')
    command = 'pip3 install -r requirement/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    for line in iter(p.stdout.readline, b''):
        print(line.decode())
    p.stdout.close()
    p.wait()
    try:
        from script.install.building import init_db
    except Exception as e:
        print(e)
        print('pip包构建失败')
        return
    print('构建数据库中..')
    init_db.build_db()
    print('Complete!')


start()
