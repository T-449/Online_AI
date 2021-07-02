# Generated by Django 3.2.3 on 2021-07-02 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game_creator', '0013_alter_game_game_title'),
        ('tournament', '0005_rename_game_tournamentinfo_game_id'),
        ('submission', '0002_alter_submission_submission_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='TournamentSubmissionEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_creator.game')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.tournamentinfo')),
            ],
        ),
    ]
