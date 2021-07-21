# Generated by Django 3.2.5 on 2021-07-21 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='JobStatus', max_length=256)),
                ('need_to_reload', models.BooleanField(default=True)),
            ],
        ),
    ]