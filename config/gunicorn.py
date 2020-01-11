import multiprocessing
from config import server_conf

bind = f'{server_conf.HOST}:{str(server_conf.WSGI_PORT)}'

timeout = 30

worker_class = 'gevent'

workers = multiprocessing.cpu_count() * 2 + 1

threads = 3

worker_connections = 1000
