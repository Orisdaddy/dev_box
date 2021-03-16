import hashlib
import getpass

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.management.commands import createsuperuser
from user.models import User


PASSWORD_FIELD = 'password'


class Command(createsuperuser.Command):
    def handle(self, *args, **options):
        user_context = {
            'username': None,
            'password': None
        }
        while True:
            username = input('用户名:')
            if User.objects.filter(username=username):
                self.stderr.write('用户名被占用！')
            else:
                user_context['username'] = username
                break

        while True:
            password = getpass.getpass('password:', )
            password_again = getpass.getpass('password (again):')
            if password != password_again:
                self.stderr.write('两次密码不一致！')
            else:
                user_context['password'] = hashlib.sha256(password.encode('utf-8')).hexdigest()
                break

        User.objects.create_superuser(username=user_context['username'], password=user_context['password'])
        self.stdout.write('创建完成')
