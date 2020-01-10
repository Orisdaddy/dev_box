FROM python:3.6.7

RUN yum -y install mysql-devel
RUN python3 build.py

CMD ['python3', 'run_server.py']
