from django.db import models
from game_creator.models import Game


# Create your models here.

class TournamentInfo(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=36, null=False, default="MyTournament")
    description = models.CharField(max_length=330, null=True)
    startTime = models.DateTimeField(null=True)
    endTime = models.DateTimeField(null=True)
    phase = models.CharField(max_length=20, null=False, default="Registration")
