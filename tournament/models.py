import django.contrib.auth.models
from django.db import models
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
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=36, null=False, default="MyTournament")
    description = models.CharField(max_length=330, null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    phase = models.CharField(max_length=20, null=False, default="Registration")
    tournament_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    tournament_type = models.CharField(max_length=15, null=False, default="roundrobin")
    max_match_generation_limit = models.IntegerField(null=False, default=3)

    objects = TournamentManager()


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
