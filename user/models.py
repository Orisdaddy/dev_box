from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    authority = models.CharField(max_length=512, null=True, default='[]')
    parent = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username
