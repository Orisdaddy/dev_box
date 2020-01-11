from config import server_conf
import subprocess
import redis
import sys

conn = redis.Redis(host=server_conf.REDIS_HOST, db=2, decode_responses=True)
CMD = [
    'start', 'stop', 'restart'
]


def start_server():
    pg = subprocess.Popen(
        'gunicorn -c config/gunicorn.py djangoDT.wsgi:application',
        shell=True,
        stdin=sys.stdin,
        stdout=sys.stdout
    )
    pd = subprocess.Popen(
        f'daphne -b {server_conf.HOST} -p {server_conf.ASGI_PORT} djangoDT.asgi:application',
        shell=True,
        stdin=sys.stdin,
        stdout=sys.stdout
    )
    conn.set('g_pid', pg.pid)
    conn.set('d_pid', pd.pid)


def stop_server():
    g_pid = conn.get('g_pid')
    d_pid = conn.get('d_pid')
    if g_pid and d_pid:
        subprocess.call(f'kill {g_pid} & kill {d_pid}', shell=True)


def restart_server():
    stop_server()

    start_server()


if __name__ == '__main__':
    try:
        cmd = sys.argv[1]
        if cmd.isdigit():
            raise IndexError
        if cmd.lower() not in CMD:
            raise IndexError
    except IndexError:
        print('请指定操作 start/stop/restart')
        sys.exit()
    if cmd.lower() == 'start':
        start_server()
    elif cmd.lower() == 'stop':
        stop_server()
    elif cmd.lower() == 'restart':
        restart_server()
    else:
        print('请指定操作 start/stop/restart')
        sys.exit()
