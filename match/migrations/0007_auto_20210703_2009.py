# Generated by Django 3.2.4 on 2021-07-03 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0006_match_history_filepath'),
    ]

    operations = [
        migrations.AddField(
            model_name='workspacematchtable',
            name='time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='history_filepath',
            field=models.FilePathField(null=True),
        ),
    ]
