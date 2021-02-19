import pymysql
from django.conf import settings
from django.core.management import execute_from_command_line


def create_database():
    db_conf = settings.DATABASES.get('default')
    conn = pymysql.connect(
        host=db_conf.get('HOST', '127.0.0.1'),
        user=db_conf.get('USER', 'root'),
        password=db_conf.get('PASSWORD'),
        charset='utf8mb4'
    )

    sql = "CREATE DATABASE IF NOT EXISTS %s" % db_conf.get('NAME')
    cursor = conn.cursor()
    cursor.execute(sql)


def migrate():
    execute_from_command_line([settings.BASE_DIR + '/manage.py', 'migrate'])


def build_db():
    create_database()
    migrate()