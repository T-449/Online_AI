from django.contrib import admin

# Register your models here.
from tournament.models import TournamentInfo

admin.site.register(TournamentInfo)
