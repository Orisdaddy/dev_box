# DevBox

后端部分(djangorestframework)

整合程序员开发工具的一款在线开发者平台



## 环境准备

python ^3.6

mysql ^5.6 或 mariadb ^5.5

redis



## 安装

1.安装环境python3&mysql&redis



2.启动构建程序

```shell
python3 build.py
```



3.确认服务配置

```shell
vi config/server_conf.py
```



4.启动服务

```shell
python3 run_server.py
```



## docker启动

1.安装环境docker&mysql&redis



2.构建docker容器

```shell
docker build --tag=dev_box .
```



3.启动容器

```shell
# -p 端口映射 宿主机开放端口:容器中服务端口
docker run -p 80:80 -p 8000:8000 dev_box
```



