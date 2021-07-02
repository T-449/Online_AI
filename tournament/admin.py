from django.contrib import admin

# Register your models here.
from tournament.models import TournamentInfo
from tournament.models import TournamentCreatorWorkspaceACL

admin.site.register(TournamentInfo)
admin.site.register(TournamentCreatorWorkspaceACL)