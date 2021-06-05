from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Game


# Create your views here.

def show_workspace_home(request, workspace_id):
    question = get_object_or_404(Game, game_uuid=workspace_id)

    return render(request, 'game_creator/game_creator_workspace.html')
