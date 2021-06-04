from django.shortcuts import render


# Create your views here.

def show_workspace_home(request, workspace_id):
    return render(request, 'game_creator/test.html')
