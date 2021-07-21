import os.path
import uuid

import game_creator.models
from Online_AI import settings
from myutils import fileutils
from django.db import models
from game_creator.models import Game
from game_creator.models import GameCreatorWorkspaceACL

from tournament.models import Tournament

import django.contrib.auth.models


# Create your models here.
class SubmissionManager(models.Manager):
    def create_test_submission(self, user, time, code, language, workspace, tag):
        submission = self.create(user=user, submission_time=time,
                                 submission_visibility=Submission.SubmissionVisibility.TEST,
                                 submission_language=language)

        fileutils.write_string_to_file(submission.get_submission_filepath(), code)

        try:
            WorkspaceTestSubmissionEntry.objects.create(game=workspace, submission=submission, tag=tag)
        except:
            Submission.objects.filter(pk=submission.pk).delete()

        return submission

    def create_tournament_submission(self, user, time, code, language, tournament):
        submission = self.create(user=user, submission_time=time,
                                 submission_visibility=Submission.SubmissionVisibility.PRIVATE,
                                 submission_language=language)

        fileutils.write_string_to_file(submission.get_submission_filepath(), code)

        try:
            TournamentSubmissionEntry.objects.create(tournament=tournament, submission=submission)
        except:
            Submission.objects.filter(pk=submission.pk).delete()

        return submission


class Submission(models.Model):
    class SubmissionVisibility(models.IntegerChoices):
        PUBLIC = 0
        PRIVATE = 1
        TEST = 2

    submission_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    submission_time = models.DateTimeField(null=True)
    user = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE)
    submission_language = models.CharField(max_length=10, default='')
    submission_visibility = models.IntegerField(choices=SubmissionVisibility.choices,
                                                default=SubmissionVisibility.PRIVATE, null=False)

    objects = SubmissionManager()

    def upload_submission_file_from_string(self, string):
        fileutils.write_string_to_file(self.get_submission_filepath(), string)

    def get_submission_url(self):
        return 'raw/' + str(self.submisson_uuid)

    def get_submission_filepath(self):
        return os.path.join(settings.MEDIA_ROOT, 'submissions', str(self.submission_uuid))

    def validate_access(self, user):
        if self.submission_visibility == Submission.SubmissionVisibility.PRIVATE:
            return self.user == user
        elif self.submission_visibility == Submission.SubmissionVisibility.TEST:
            game = WorkspaceTestSubmissionEntry.objects.get(submission=self).game
            return game_creator.models.game_creator_validate_workspace_access(user, game)
        else:
            return True

    @property
    def getWorkspaceTestSubmissionTag(self):
        try:
            return WorkspaceTestSubmissionEntry.objects.get(submission=self).tag;
        except WorkspaceTestSubmissionEntry.DoesNotExist as e:
            return None

    @property
    def getDescription(self):
        ans = self.user.username;
        if self.submission_visibility == Submission.SubmissionVisibility.TEST:
            ans += " (" + self.getWorkspaceTestSubmissionTag + ")"
        return ans


class WorkspaceTestSubmissionEntry(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    tag = models.CharField(max_length=100, default="")
    is_test = models.BooleanField(default=False, null=False)


class TournamentSubmissionEntry(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)

# from submission.models import Submission
# from django.contrib.auth.models import User
# from game_creator.models import Game
# u = User.objects.get(pk=1)
# g = Game.objects.get(pk=1)
# lang='c++'
# import datetime
# dt = datetime.datetime.now()
# code='hello'
# c = Submission.objects.create_test_submission(u,dt,code,lang,g)
