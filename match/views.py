from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

import game_creator
from match.models import Match
from submission.models import Submission


def post_create_match(request, workspace_uuid):
    game = game_creator.views.get_game_or_validate_requests(request, workspace_uuid)

    try:
        submission0 = Submission.objects.get(submission_uuid=request.POST['submission0'])
        submission1 = Submission.objects.get(submission_uuid=request.POST['submission1'])
    except:
        raise Http404

    user = request.user
    if not submission0.validate_access(user) or not submission1.validate_access(user):
        raise Http404

    Match.objects.create_test_match(submission0, submission1, game)
    r = HttpResponseRedirect(reverse('game_creator_show_workspace', args=(workspace_uuid,)))
    messages.success(request, 'Saved')

    return r