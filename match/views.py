import os
import threading
from multiprocessing import Queue, Process

from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from match import models
from matchExecutionUnit.matchExecutionUnit import execute_match
from myutils import fileutils
# Create your views here.
from django.urls import reverse

import game_creator
from match.models import Match
from myutils.httputils import redirectToCurrent
from submission.models import Submission


def post_create_match(request, workspace_uuid):
    game = game_creator.views.get_game_or_validate_requests(request, workspace_uuid)

    try:
        submission0 = Submission.objects.get(submission_uuid=request.POST['submission0'].strip())
        submission1 = Submission.objects.get(submission_uuid=request.POST['submission1'].strip())
    except:
        raise Http404

    user = request.user
    if not submission0.validate_access(user) or not submission1.validate_access(user):
        raise Http404

    Match.objects.create_test_match(submission0, submission1, game)
    r = HttpResponseRedirect(reverse('game_creator_show_workspace', args=(workspace_uuid,)))
    messages.success(request, 'Saved')

    return r


def get_match_or_validate_requests(request, match_uuid):
    match = get_object_or_404(Match, match_uuid=match_uuid)

    if not match.validate_request(request):
        raise Http404
    return match

def get_match_or_validate_judge_requests(request, match_uuid):
    match = get_object_or_404(Match, match_uuid=match_uuid)

    if not match.validate_judge_request(request):
        raise Http404
    return match


def show_match_history(request, match_uuid):
    match = get_match_or_validate_requests(request, match_uuid)
    match_history = fileutils.get_file_content_as_string(match.history_filepath).encode('unicode_escape').decode('utf-8')
    match_result = match.match_results
    match_status = match.match_status
    visualizer = fileutils.get_file_content_as_string(match.game.get_visualization_code_filepath())
    iframe_src_doc = "<html><head><meta charset=\"UTF-8\"><script type=\"text/javascript\"> " + visualizer + \
                     "</script></head> <body>  <script> document.body.onload=function() {" \
                     "test(\'" + match_history + "\');}</script><div id=\"visualizer\"></div></body></html>"
    print(iframe_src_doc)

    if match.match_results is not None:
        if match.match_results == "win":
            match_result = "Player 1(" + match.submission0.user.username + ") won"
        elif match.match_results == "Player":
            match_result = "Player 2(" + match.submission1.user.username + ") won"
        elif match.match_results == "draw":
            match_result = "The Game drawn"
        else:
            match_result = "Error"

    context = {
        "match": match,
        "result": match_result,
        "match_history": match_history,
        "iframe_src_doc": iframe_src_doc
    }
    return render(request, 'match/match_history.html', context)


def judge_match(request, match_uuid):
    match = get_match_or_validate_judge_requests(request, match_uuid)

    p = Process(target=execute_match, args=(match,))
    p.start()

    return redirectToCurrent(request)

def delete_match(request, match_uuid):
    match = get_match_or_validate_judge_requests(request, match_uuid)
    try:
        os.remove(match.history_filepath)
    except IsADirectoryError:
        pass
    models.Match.objects.filter(match_uuid=match_uuid).delete()
    return redirectToCurrent(request)
