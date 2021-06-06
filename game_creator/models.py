import errno
import uuid
import os

import django.contrib.auth.models
from django.db import models
from Online_AI import settings


# Create your models here.
class GameManager(models.Manager):
    def create_game(self, user):
        game = self.create()
        initialize_with_empty_file(game.get_game_description_filepath())
        initialize_with_empty_file(game.get_game_judge_code_filepath())
        initialize_with_empty_file(game.get_visualization_code_filepath())

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
        write_string_to_file(self.get_game_judge_code_filepath(), string)

    def upload_description_file(self, f):
        with open(self.get_game_description_filepath(), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    def upload_description_file_from_string(self, string):
        write_string_to_file(self.get_game_description_filepath(), string)

    def upload_visualization_file_from_string(self, string):
        write_string_to_file(self.get_visualization_code_filepath(), string)

    def get_judge_code_url(self):
        return str(self.game_uuid) + '/raw/judge_code'

    def get_game_judge_code_filepath(self):
        return os.path.join(settings.MEDIA_ROOT, str(self.game_uuid) + '/judge_code')

    def get_game_description_url(self):
        return str(self.game_uuid) + '/raw/description'

    def get_game_description_filepath(self):
        return os.path.join(settings.MEDIA_ROOT, str(self.game_uuid) + '/description')

    def get_visualization_code_url(self):
        return str(self.game_uuid) + '/raw/visualization_code'

    def get_visualization_code_filepath(self):
        return os.path.join(settings.MEDIA_ROOT, str(self.game_uuid) + '/visualization_code')

    def __str__(self):
        return super().__str__() + " {uuid : " + str(self.game_uuid) + "}"


def initialize_with_empty_file(filename):
    write_string_to_file(filename, '')


def write_string_to_file(filename, string):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, "w") as f:
        # for c
        f.write(string)
        f.close()


class GameCreatorWorkspaceACL(models.Model):
    user = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'game',)


def game_creator_validate_workspace_access(user, game):
    try:
        GameCreatorWorkspaceACL.objects.get(user=user, game=game)
        return True
    except (KeyError, GameCreatorWorkspaceACL.DoesNotExist):
        return False
    return False
