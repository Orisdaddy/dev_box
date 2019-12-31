from django.db import models
from user.models import User


class PostManHistory(models.Model):
    host = models.CharField(max_length=64)
    method = models.CharField(max_length=12)
    params = models.TextField(max_length=10240, null=True)
    body = models.TextField(max_length=10240, null=True)
    headers = models.TextField(max_length=10240, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.method + '  ' + self.host


class Services(models.Model):
    host = models.CharField(max_length=32)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.host
