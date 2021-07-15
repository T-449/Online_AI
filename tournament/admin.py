from django.contrib import admin

# Register your models here.
from tournament.models import Tournament
from tournament.models import TournamentCreatorACL

admin.site.register(Tournament)
admin.site.register(TournamentCreatorACL)