# Generated by Django 3.2.3 on 2021-06-05 21:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game_creator', '0011_auto_20210605_2119'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='gamecreatorworkspaceacl',
            unique_together={('user', 'game')},
        ),
    ]
