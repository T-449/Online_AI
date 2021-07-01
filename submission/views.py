import os

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse

import game_creator
from . import models
from django.shortcuts import get_object_or_404


# Create your views here.
def get_submission_or_validate_requests(request, submission_uuid):
    submission = get_object_or_404(models.Submission, submission_uuid=submission_uuid)
    if not request.user.is_authenticated or \
            not submission.validate_access(request.user):
        raise Http404
    return submission


def show_raw_submission(request, submission_uuid):
    submission = get_submission_or_validate_requests(request, submission_uuid)
    file_path = submission.get_submission_filepath()

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/plain")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def post_test_submission(request, workspace_uuid):
    game = game_creator.views.get_game_or_validate_requests(request, workspace_uuid)

    lang = request.POST['submission_language']
    code = request.POST['submission_code']
    time = request.POST['submission_time']
    user = request.user
    submission = models.Submission.objects.create_test_submission(user, time, code, lang, game)
    r = HttpResponseRedirect(reverse('game_creator_show_workspace', args=(workspace_uuid,)))
    messages.success(request, 'Saved')
    return r
