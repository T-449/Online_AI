import errno
import uuid
import os

import django.contrib.auth.models
from django.db import models
from myutils import fileutils

import game_creator.models
from Online_AI import settings


# Create your models here.
class GameManager(models.Manager):
    def create_game(self, user):
        game = self.create()
        fileutils.initialize_with_empty_file(game.get_game_description_filepath())
        fileutils.initialize_with_empty_file(game.get_game_judge_code_filepath())
        fileutils.initialize_with_empty_file(game.get_visualization_code_filepath())

        try:
            GameCreatorWorkspaceACL.objects.create(user=user, game=game)
        except:
            Game.objects.filter(pk=game.pk).delete()

        return game


class Game(models.Model):
    game_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    game_judge_code_language = models.CharField(max_length=10, default='')
    game_visualization_code_language = models.CharField(max_length=10, default='')

    # game_judge_code_file_path = models.CharField(max_length=256, default='')
    # description_file_path = models.CharField(max_length=256, default='')

    objects = GameManager()

    game_title = models.CharField(max_length=256, default='Untitled')

    def upload_judge_code(self, f, language):
        with open(settings.MEDIA_ROOT + "/" + self.get_judge_code_url(), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        self.game_judge_code_language = language
        self.save()

    def upload_judge_code_from_string(self, string):
        fileutils.write_string_to_file(self.get_game_judge_code_filepath(), string)

    def upload_description_file(self, f):
        with open(self.get_game_description_filepath(), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    def upload_description_file_from_string(self, string):
        fileutils.write_string_to_file(self.get_game_description_filepath(), string)

    def upload_visualization_file_from_string(self, string):
        fileutils.write_string_to_file(self.get_visualization_code_filepath(), string)

    def get_game_judge_code_filepath(self):
        return os.path.join(settings.MEDIA_ROOT, 'workspace/' + str(self.game_uuid) + '/judge_code')

    def get_game_description_filepath(self):
        return os.path.join(settings.MEDIA_ROOT, 'workspace/' + str(self.game_uuid) + '/description')

    def get_visualization_code_filepath(self):
        return os.path.join(settings.MEDIA_ROOT, 'workspace/' + str(self.game_uuid) + '/visualization_code')

    def __str__(self):
        return super().__str__() + " {uuid : " + str(self.game_uuid) + "}"


class GameCreatorWorkspaceACL(models.Model):
    user = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'game',)


# class GameCreatorWorkspaceInvite(models.Model):
#     access_entry = models.ForeignKey(GameCreatorWorkspaceACL, on_delete=models.CASCADE)
#
#     def reject_invite(self):


def game_creator_validate_workspace_access(user, game):
    try:
        GameCreatorWorkspaceACL.objects.get(user=user, game=game)
        return True
    except (KeyError, GameCreatorWorkspaceACL.DoesNotExist):
        return False
    return False

# class SubmissionManager(models.Manager):
#    def create_test_submission(self, user, language, code, time, workspace):
#        game = self.create()
#        initialize_with_empty_file(game.get_game_description_filepath())
#        initialize_with_empty_file(game.get_game_judge_code_filepath())
#        initialize_with_empty_file(game.get_visualization_code_filepath())
#
#        try:
#            GameCreatorWorkspaceACL.objects.create(user=user, game=game)
#        except:
#            Game.objects.filter(pk=game.pk).delete()
#
#        return game
#

# class Submission(models.Model):
#     submission_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
#     submission_time = models.DateTimeField()
#     user = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE)
#     submission_language = models.CharField(max_length=10, default='')
#
#     def upload_submission_file_from_string(self, string):
#         write_string_to_file(self.get_submission_filepath(), string)
#
#     def get_judge_code_url(self):
#         return str(self.submisson_uuid)
#
#     def get_game_judge_code_filepath(self):
#         return os.path.join(settings.MEDIA_ROOT, 'workspace/' + str(self.game_uuid) + '/judge_code')
#
#
# class WorkspaceTestSubmissionEntry(models.Model):
#     submission = models.ForeignKey(game_creator.models.Game, on_delete=models.CASCADE)
#     game = models.ForeignKey(game_creator.models.Game, on_delete=models.CASCADE)
