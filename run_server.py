from config import server_conf
import subprocess
import sys
import os

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoDT.settings')
if __name__ == '__main__':
    subprocess.Popen(
        'gunicorn -c config/gunicorn.py djangoDT.wsgi:application',
        shell=True,
        stdin=sys.stdin,
        stdout=sys.stdout
    )
    print('启动daphne')
    subprocess.Popen(
        f'daphne -b {server_conf.HOST} -p {server_conf.ASGI_PORT} djangoDT.asgi:application',
        shell=True,
        stdin=sys.stdin,
        stdout=sys.stdout
    )

