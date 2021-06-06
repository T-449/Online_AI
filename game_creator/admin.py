from django.contrib import admin

from .models import Game, GameCreatorWorkspaceACL

# Register your models here.

admin.site.register(Game)
admin.site.register(GameCreatorWorkspaceACL)
