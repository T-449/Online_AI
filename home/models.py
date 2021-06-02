from django.db import models


# Create your models here.

class UserInfo(models.Model):
    username = models.CharField(max_length=256, null=True)
    password = models.CharField(max_length=256, null=True)
