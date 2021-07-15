import django.contrib.auth.models
from django.db import models
from game_creator.models import Game


# Create your models here.

class Tournament(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=36, null=False, default="MyTournament")
    description = models.CharField(max_length=330, null=True)
    startTime = models.DateTimeField(null=True)
    endTime = models.DateTimeField(null=True)
    phase = models.CharField(max_length=20, null=False, default="Registration")


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
    return False
