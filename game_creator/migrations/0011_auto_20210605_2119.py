# Generated by Django 3.2.3 on 2021-06-05 21:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_creator', '0010_gamecreatorworkspaceacl'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gamecreatorworkspaceacl',
            old_name='game_id',
            new_name='game',
        ),
        migrations.RenameField(
            model_name='gamecreatorworkspaceacl',
            old_name='user_id',
            new_name='user',
        ),
    ]