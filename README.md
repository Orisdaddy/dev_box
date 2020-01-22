<div align="center">
    <img src="static/faviconmin.png"/>
</div>

# DevBox

后端(djangorestframework)

前端(Vue) https://github.com/824750130/dev_box_vue.git

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
# 启动服务
python3 devsm.py start
# 关闭服务
python3 devsm.py stop
# 重启服务
python3 devsm.py restart
```


5.创建用户
```shell
python3 manage.py createsuperuser
```



### docker启动

1.安装环境docker&mysql&redis



2.构建docker容器

```shell
docker build --tag=dev_box .
```



3.启动容器

```shell
# -p 端口映射 宿主机开放端口:容器中服务端口
docker run -p 8001:8001 -p 8000:8000 dev_box
```



## 功能介绍

<table style="width: 882px">
  <thead style="text-align: center">
    <tr>
      <th>模块</th>
      <th>功能</th>
      <th>进度</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>API接口调试&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</td>
      <td>API接口调试&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</td>
      <td>已完成&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</td>
    </tr>
    <tr>
      <td rowspan="2">远程Linux操作</td>
      <td>交互式终端</td>
      <td>待测试</td>
    </tr>
    <tr>
      <td>Sftp文件传输</td>
      <td>待完善</td>
    </tr>
    <tr>
      <td rowspan="2">数据库连接模块</td>
      <td>SQL数据库</td>
      <td>待开发</td>
    </tr>
    <tr>
      <td>NO SQL数据库</td>
      <td>待开发</td>
    </tr>
    <tr>
      <td>markdown文档管理</td>
      <td>markdown文档管理</td>
      <td>待开发</td>
    </tr>
    <tr>
      <td>项目管理</td>
      <td>项目管理</td>
      <td>待开发</td>
    </tr>
  </tbody>
</table>

