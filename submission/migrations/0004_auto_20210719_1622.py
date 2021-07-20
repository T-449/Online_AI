# Generated by Django 3.2.3 on 2021-07-19 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0003_alter_tournamentsubmissionentry_submission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='submission_status',
        ),
        migrations.AddField(
            model_name='submission',
            name='submission_visibility',
            field=models.IntegerField(choices=[(0, 'Public'), (1, 'Private'), (2, 'Test')], default=1),
        ),
    ]