# Generated by Django 3.2.3 on 2021-07-02 15:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('game_creator', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TournamentInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='MyTournament', max_length=36)),
                ('description', models.CharField(max_length=330, null=True)),
                ('startTime', models.DateTimeField(null=True)),
                ('endTime', models.DateTimeField(null=True)),
                ('phase', models.CharField(default='Registration', max_length=20)),
                ('game_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_creator.game')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentParticipantWorkspaceACL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.tournamentinfo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'tournament')},
            },
        ),
        migrations.CreateModel(
            name='TournamentCreatorWorkspaceACL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.tournamentinfo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'tournament')},
            },
        ),
    ]
