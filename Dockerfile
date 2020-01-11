FROM python:3.6.7

WORKDIR /opt/dev_box
COPY . /opt/dev_box

RUN python3 docker_build.py

CMD python3 devsm.py start
