# Generated by Django 3.2.4 on 2021-07-03 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workspacetestsubmissionentry',
            name='tag',
            field=models.CharField(default='', max_length=100),
        ),
    ]