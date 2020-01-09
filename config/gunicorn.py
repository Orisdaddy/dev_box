import multiprocessing

bind = '0.0.0.0:80'
# 宕机30秒重启
timeout = 30
# 工作模式
worker_class = 'gevent'


# worker数量推荐 机器核心数*2+1
workers = multiprocessing.cpu_count() * 2 + 1
# 线程数推荐 2-4
threads = 3
# 最大并发连接数默认1000
worker_connections = 1000