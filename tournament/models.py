import datetime

import django.contrib.auth.models
from django.db import models
from django.utils import timezone
from game_creator.models import Game
import uuid


# Create your models here.

class TournamentManager(models.Manager):
    def create_tournament(self, creator, game, name, description, start_time, end_time, phase, tournament_type,
                          max_match_generation_limit):
        tournament = self.create(game=game, name=name, description=description,
                                 start_time=start_time, end_time=end_time, phase=phase, tournament_type=tournament_type,
                                 max_match_generation_limit=max_match_generation_limit)
        try:
            TournamentCreatorACL.objects.create(user=creator, tournament=tournament)
        except:
            Tournament.objects.filter(pk=tournament.pk).delete()
            return None
        return tournament


class Tournament(models.Model):
    class TournamentPhase(models.TextChoices):
        OPEN_FOR_REGISTRATION = 'reg'
        OPEN_FOR_SUBMISSION = 'sub'
        MATCH_EXECUTION = 'exec'
        TOURNAMENT_ENDED = 'end'

    class TournamentType(models.TextChoices):
        ROUND_ROBIN = 'rr'

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=36, null=False)
    description = models.CharField(max_length=330, null=False, default="")
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    phase = models.CharField(max_length=5, choices=TournamentPhase.choices,
                             default=TournamentPhase.OPEN_FOR_REGISTRATION)
    tournament_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    tournament_type = models.CharField(max_length=6, choices=TournamentType.choices, default=TournamentType.ROUND_ROBIN)
    max_match_generation_limit = models.IntegerField(null=False, default=3)

    objects = TournamentManager()

    @property
    def shouldHaveStarted(self):
        return timezone.now() >= self.start_time

    @property
    def shouldHaveEnded(self):
        return timezone.now() >= self.end_time

    @property
    def shouldBeRunning(self):
        return self.shouldHaveStarted and not self.shouldHaveEnded

    @property
    def getTypeName(self):
        return self.TournamentType(self.tournament_type).name

class TournamentCreatorACL(models.Model):
    user = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'tournament',)


def is_tournament_creator(user, tournament):
    try:
        TournamentCreatorACL.objects.get(user=user, tournament=tournament)
        return True
    except (KeyError, TournamentCreatorACL.DoesNotExist):
        return False


class TournamentRegistration(models.Model):
    user = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'tournament',)


def is_user_registered_in_tournament(user, tournament):
    try:
        TournamentRegistration.objects.get(user=user, tournament=tournament)
        return True
    except (KeyError, TournamentRegistration.DoesNotExist):
        return False
