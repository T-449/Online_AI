import uuid
from django.db import models
from Online_AI import settings


# Create your models here.


class Game(models.Model):
    game_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    game_judge_code_language = models.CharField(max_length=10, default='')
    # game_judge_code_file_path = models.CharField(max_length=256, default='')
    # description_file_path = models.CharField(max_length=256, default='')

    game_title = models.CharField(max_length=256, default='')

    def upload_judge_code(self, f, language):
        with open(settings.MEDIA_ROOT + "/" + self.game_uid.hex() + "/judge_code", 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        self.game_judge_code_language = language
        self.save()

    def upload_description_file(self, f):
        with open(settings.MEDIA_ROOT + "/" + self.game_uid.hex() + "/judge_code", 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
