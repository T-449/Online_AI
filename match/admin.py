from django.contrib import admin

# Register your models here.
from match.models import Match, TournamentMatchTable, WorkspaceMatchTable

admin.site.register(Match)
admin.site.register(TournamentMatchTable)
admin.site.register(WorkspaceMatchTable)
