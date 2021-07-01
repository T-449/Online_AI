import os

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib import messages

import submission.views
from .models import Game, GameCreatorWorkspaceACL, game_creator_validate_workspace_access
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from submission.models import WorkspaceTestSubmissionEntry

from django.contrib.auth.models import User


# Create your views here.

def get_game_or_validate_requests(request, workspace_id):
    game = get_object_or_404(Game, game_uuid=workspace_id)
    if not request.user.is_authenticated or \
            not game_creator_validate_workspace_access(request.user, game):
        raise Http404
    return game


def show_workspace_home(request, workspace_id):
    game = get_game_or_validate_requests(request, workspace_id)
    print(game.game_title)
    qs = GameCreatorWorkspaceACL.objects.filter(game=game)
    workspace_agent_entries = WorkspaceTestSubmissionEntry.objects.filter(game=game)
    return render(request, 'game_creator/game_creator_workspace.html', {'game': game, 'query_list': qs,
                                                                        'workspace_agent_entries': workspace_agent_entries})


def post_game_description(request, workspace_id):
    game = get_game_or_validate_requests(request, workspace_id)
    r = HttpResponseRedirect(reverse('game_creator_show_workspace', args=(workspace_id,)))
    print(type(request.POST['description']))
    game.upload_description_file_from_string(request.POST['description'])
    game.game_title = request.POST['title']
    game.save()
    messages.success(request, 'Saved')
    return r


def post_judge_code(request, workspace_id):
    game = get_game_or_validate_requests(request, workspace_id)
    r = HttpResponseRedirect(reverse('game_creator_show_workspace', args=(workspace_id,)))
    game.upload_judge_code_from_string(request.POST['judge_code'])
    game.game_judge_code_language = request.POST['judge_code_language']
    game.save()
    messages.success(request, 'Saved')
    return r


def post_visualization_code(request, workspace_id):
    game = get_game_or_validate_requests(request, workspace_id)
    r = HttpResponseRedirect(reverse('game_creator_show_workspace', args=(workspace_id,)))
    game.upload_visualization_file_from_string(request.POST['visualization_code'])
    game.game_visualization_code_language = request.POST['visualization_language']
    game.save()
    messages.success(request, 'Saved')
    return r


def post_add_agent(request, workspace_id):
    return submission.views.post_test_submission(request, workspace_id)


def get_game_description(request, game_uuid):
    game = get_game_or_validate_requests(request, game_uuid)
    file_path = game.get_game_description_filepath()

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/plain")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def get_game_judge_code(request, game_uuid):
    game = get_game_or_validate_requests(request, game_uuid)
    file_path = game.get_game_judge_code_filepath()
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/plain")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def get_game_visualization_code(request, game_uuid):
    game = get_game_or_validate_requests(request, game_uuid)
    file_path = game.get_visualization_code_filepath()
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/plain")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def send_invite(request, workspace_id):
    game = get_game_or_validate_requests(request, workspace_id)
    try:
        invited = User.objects.get(username=request.POST['user_invite'])
        print(workspace_id)
        GameCreatorWorkspaceACL.objects.create(user=invited, game=game)
    except:
        raise Http404

    messages.success(request, 'invite sent')
    return HttpResponseRedirect(reverse('game_creator_show_workspace', args=(workspace_id,)))
