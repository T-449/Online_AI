from django.db import models


# Create your models here.

class UserInfo(models.Model):
    firstname = models.CharField(max_length=256, null=True)
    lastname = models.CharField(max_length=256, null=True)
    username = models.CharField(max_length=256, null=True)
    password = models.CharField(max_length=256, null=True)
    email = models.EmailField(max_length=256, null=True)
    country = models.CharField(max_length=14, null=True)
