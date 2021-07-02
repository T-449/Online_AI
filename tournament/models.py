import django.contrib.auth.models
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


class TournamentCreatorWorkspaceACL(models.Model):
    user = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(TournamentInfo, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'tournament',)


def tournament_creator_validate_workspace_access(user, tournament):
    try:
        TournamentCreatorWorkspaceACL.objects.get(user=user, tournament=tournament)
        return True
    except (KeyError, TournamentCreatorWorkspaceACL.DoesNotExist):
        return False
    return False


class TournamentParticipantWorkspaceACL(models.Model):
    user = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(TournamentInfo, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'tournament',)


def tournament_participant_validate_workspace_access(user, tournament):
    try:
        TournamentParticipantWorkspaceACL.objects.get(user=user, tournament=tournament)
        return True
    except (KeyError, TournamentParticipantWorkspaceACL.DoesNotExist):
        return False
    return False
