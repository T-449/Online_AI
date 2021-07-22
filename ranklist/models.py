import django.contrib.auth.models
from django.db import models

# Create your models here.
from submission.models import Submission
from tournament.models import Tournament


class Ranklist(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    rank = models.IntegerField(null=False, default=0)
