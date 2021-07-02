import os
import uuid

from django.db import models

from Online_AI import settings
from submission.models import Submission
from game_creator.models import Game
from tournament.models import TournamentInfo


# Create your models here.

class MatchManager(models.Manager):
    def create_tournament_match(self, submission0, submission1, tournament):
        match = self.create(submission0=submission0, submission1=submission1, game=tournament.game_id)

        try:
            TournamentMatchTable.objects.create(tournament=tournament, match=match)
        except:
            TournamentMatchTable.objects.filter(pk=match.pk).delete()

        return match

    def create_test_match(self, submission0, submission1, workspace):
        match = self.create(submission0=submission0, submission1=submission1, game=workspace)

        try:
            WorkspaceMatchTable.objects.create(workspace=workspace, match=match)
        except:
            WorkspaceMatchTable.objects.filter(pk=match.pk).delete()

        return match


class Match(models.Model):
    match_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    match_phase = models.CharField(max_length=10, null=False, default='waiting')
    submission0 = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='player0_submission')
    submission1 = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='player1_submission')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    objects = MatchManager()

    def get_match_history_filepath(self):
        return os.path.join(settings.MEDIA_ROOT, 'matches/' + str(self.match_uuid))

class TournamentMatchTable(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    tournament = models.ForeignKey(TournamentInfo, on_delete=models.CASCADE)


class WorkspaceMatchTable(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Game, on_delete=models.CASCADE)
