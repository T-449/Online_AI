# Generated by Django 3.2.3 on 2021-06-04 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_creator', '0007_auto_20210604_1859'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='game_uid',
            new_name='game_uuid',
        ),
    ]
