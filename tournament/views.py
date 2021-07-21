import traceback
from datetime import datetime

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404

from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.utils.timezone import get_default_timezone, get_current_timezone, make_aware

from Online_AI import settings
from Online_AI.settings import MAX_TEST_GENERATION_LIMIT
from game_creator.models import Game, GameCreatorWorkspaceACL
from match.models import Match, TournamentTestMatchTable
from myutils.fileutils import get_file_content_as_string
from tournament.models import Tournament, TournamentCreatorACL, TournamentRegistration
from submission.models import Submission, TournamentSubmissionEntry, WorkspaceTestSubmissionEntry
from itertools import chain


# Create your views here.

def create_tournament(request):
    games = GameCreatorWorkspaceACL.objects.filter(user_id=request.user.id)
    gameList = []
    for game in games:
        gameList.append(game.game)
    tournament_types = Tournament.TournamentType.names

    context = {
        'games': gameList,
        'tournament_types': tournament_types,
        'servertime': timezone.now(),
        'MAX_TEST_GENERATION_LIMIT': MAX_TEST_GENERATION_LIMIT
    }
    return render(request, 'tournament/createTournament.html', context)


def update_tournament(request, tournament_uuid):
    tournament = Tournament.objects.get(tournament_uuid=tournament_uuid)
    games = GameCreatorWorkspaceACL.objects.filter(user_id=request.user.id)
    gameList = []
    for game in games:
        gameList.append(game.game)
    tournament_types = Tournament.TournamentType.names

    context = {
        'tournament': tournament,
        'games': gameList,
        'tournament_types': tournament_types,
        'servertime': timezone.now(),
        'MAX_TEST_GENERATION_LIMIT': MAX_TEST_GENERATION_LIMIT
    }
    return render(request, 'tournament/updateTournament.html', context)


def post_create_tournament(request):
    givendate = request.POST['startdate'].split('-')
    giventime = request.POST['starttime'].split(':')
    start_time = datetime(int(givendate[0]), int(givendate[1]), int(givendate[2]),
                          int(giventime[0]), int(giventime[1]), int(giventime[2]), 0)
    start_time = make_aware(start_time)

    givendate = request.POST['enddate'].split('-')
    giventime = request.POST['endtime'].split(':')
    end_time = datetime(int(givendate[0]), int(givendate[1]), int(givendate[2]),
                        int(giventime[0]), int(giventime[1]), int(giventime[2]), 0)
    end_time = make_aware(end_time)
    game_id = request.POST['game']

    game = Game.objects.get(pk=game_id)
    user = request.user

    try:
        tournament = Tournament.objects.create_tournament(creator=user, name=request.POST['tournamentname'], game=game,
                                                          start_time=start_time, end_time=end_time,
                                                          description=request.POST['description'],
                                                          phase=Tournament.TournamentPhase.OPEN_FOR_REGISTRATION,
                                                          tournament_type=Tournament.TournamentType[
                                                              request.POST['tournamentType']],
                                                          max_match_generation_limit=int(request.POST['maxMatches']))
    except Exception as e:
        traceback.print_exc(e)
        return HttpResponseRedirect(reverse('tournamentList'))
    return HttpResponseRedirect(reverse('show_tournament_workspace', args=(tournament.tournament_uuid,)))


def post_update_tournament(request, tournament_uuid):
    givendate = request.POST['startdate'].split('-')
    giventime = request.POST['starttime'].split(':')
    start_time = datetime(int(givendate[0]), int(givendate[1]), int(givendate[2]),
                          int(giventime[0]), int(giventime[1]), int(giventime[2]), 0)
    start_time = make_aware(start_time)

    givendate = request.POST['enddate'].split('-')
    giventime = request.POST['endtime'].split(':')
    end_time = datetime(int(givendate[0]), int(givendate[1]), int(givendate[2]),
                        int(giventime[0]), int(giventime[1]), int(giventime[2]), 0)
    end_time = make_aware(end_time)

    game_id = request.POST['game']
    game = Game.objects.get(pk=game_id)

    tournament = Tournament.objects.get(tournament_uuid=tournament_uuid)
    try:
        tournament.name = request.POST['tournamentname']
        tournament.game = game
        tournament.start_time = start_time
        tournament.end_time = end_time
        tournament.type = request.POST['tournamentType']
        tournament.max_match_generation_limit = int(request.POST['maxMatches'])
        tournament.save()
    except Exception as e:
        traceback.print_exc(e)
        HttpResponseRedirect(reverse('tournamentList'))
    return HttpResponseRedirect(reverse('show_tournament_workspace', args=(tournament.tournament_uuid,)))


def show_tournament_workspace(request, tournament_uuid):
    tournament = Tournament.objects.get(tournament_uuid=tournament_uuid)
    game = tournament.game
    game_description = get_file_content_as_string(game.get_game_description_filepath()).encode('unicode_escape'
                                                                                               ).decode('utf-8')
    visible = True
    registered = False
    if request.user.id is not None:
        if TournamentCreatorACL.objects.filter(user=request.user, tournament=tournament).exists():
            visible = False
        else:
            if TournamentRegistration.objects.filter(user=request.user,
                                                     tournament=tournament).exists():
                registered = True
    else:
        visible = False

    tournamentCreator = TournamentCreatorACL.objects.get(tournament=tournament)
    testSubmissions = WorkspaceTestSubmissionEntry.objects.all().filter(submission__user=tournamentCreator.user)
    tournament_test_matches = TournamentTestMatchTable.objects.filter(user=request.user)

    submissions = TournamentSubmissionEntry.objects.all().filter(submission__user=request.user)
    submissionList = list(chain(testSubmissions, submissions))

    return render(request, 'tournament/tournament_tabs.html',
                  {'tournament': tournament, 'game': game.game_title, 'visible': visible, 'registered': registered,
                   'tournament_test_matches': tournament_test_matches, 'game_description': game_description,
                   'entries': submissions, 'testEntries': submissionList})


def reg_unreg(request, tournament_uuid):
    val = request.POST['register']
    val = val.split()
    tournament = Tournament.objects.get(tournament_uuid=tournament_uuid)
    user = request.user

    if val[0] == 'reg':
        try:
            TournamentRegistration.objects.get(user=user, tournament=tournament)
        except:
            TournamentRegistration(user=user, tournament=tournament).save()
    else:
        try:
            TournamentRegistration.objects.get(tournament=tournament, user=user).delete()
        except Exception as e:
            traceback.print_exc(e)
    return show_tournament_workspace(request, tournament_uuid)


def tournamentList(request):
    tournaments = Tournament.objects.all()
    tournament_phases = Tournament.TournamentPhase.names
    myTournaments = TournamentCreatorACL.objects.filter(user_id=request.user.id)
    myTournamentList = []
    for tournament in myTournaments:
        myTournamentList.append(Tournament.objects.get(id=tournament.tournament_id))
    registeredTournaments = TournamentRegistration.objects.filter(user_id=request.user.id)
    registeredTournamentList = []
    for tournament in registeredTournaments:
        registeredTournamentList.append(Tournament.objects.get(id=tournament.tournament_id))
    show = False
    if request.user.id is not None:
        show = True
    return render(request, 'tournament/tournamentList.html',
                  {'tournaments': tournaments, 'show': show, 'myTournaments': myTournamentList,
                   'registeredTournaments': registeredTournamentList, 'tournament_phases': tournament_phases})


def add_submission(request, tournament_uuid):
    tournament = Tournament.objects.get(tournament_uuid=tournament_uuid)
    Submission.objects.create_tournament_submission(user=request.user,
                                                    code=request.POST['submission_code'],
                                                    language=request.POST['submission_language'],
                                                    tournament=tournament,
                                                    time=timezone.now())
    messages.success(request, "Saved")
    return show_tournament_workspace(request, tournament_uuid)


def change_phase(request, tournament_uuid):
    tournament = Tournament.objects.get(tournament_uuid=tournament_uuid)
    print(tournament.TournamentPhase.choices)
    print(tournament.TournamentPhase.values)
    print(tournament.TournamentPhase.names)
    print(tournament.TournamentPhase['OPEN_FOR_REGISTRATION'])

    try:
        tournament.phase = Tournament.TournamentPhase[request.POST['changedphase']]
        tournament.save()
    except Exception as e:
        traceback.print_exc(e)

    return HttpResponseRedirect(reverse('show_tournament_workspace', args=(tournament_uuid,)))


def tournament_post_create_test_match(request, tournament_uuid):
    tournament = get_object_or_404(Tournament, tournament_uuid=tournament_uuid)
    game = tournament.game

    r = HttpResponseRedirect(reverse('show_tournament_workspace', args=(tournament_uuid,)))

    user_matches = TournamentTestMatchTable.objects.filter(tournament=tournament, user=request.user)
    print(user_matches, len(user_matches), tournament.max_match_generation_limit)
    if len(user_matches) >= tournament.max_match_generation_limit:
        return r

    user_submissions = TournamentSubmissionEntry.objects.filter(tournament=tournament,
                                                                submission__user=request.user).values_list('submission',
                                                                                                           flat=True)

    test_agents = WorkspaceTestSubmissionEntry.objects.filter(game=game).values_list('submission', flat=True)
    try:
        submission0 = Submission.objects.get(submission_uuid=request.POST['submission0'].strip())
        submission1 = Submission.objects.get(submission_uuid=request.POST['submission1'].strip())
    except:
        raise Http404

    if submission0.pk not in user_submissions and submission0.pk not in test_agents:
        print(submission0)
        print(user_submissions)
        print(test_agents)
        raise Http404

    if submission1.pk not in user_submissions and submission1.pk not in test_agents:
        print(submission0)
        print(user_submissions)
        print(test_agents)
        raise Http404

    Match.objects.create_tournament_test_match(submission0=submission0, submission1=submission1,
                                               tournament=tournament, user=request.user)
    return r
