# Generated by Django 3.2.3 on 2021-06-04 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_creator', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='description_code',
        ),
        migrations.RemoveField(
            model_name='game',
            name='judge_code',
        ),
    ]
