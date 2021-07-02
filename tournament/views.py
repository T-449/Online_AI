from django.shortcuts import render
import random
import string
from datetime import datetime

from django.contrib.auth.models import User
from game_creator.models import Game, GameCreatorWorkspaceACL
from tournament.models import TournamentInfo, TournamentCreatorWorkspaceACL, TournamentParticipantWorkspaceACL


def generateRandomString(characters):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=characters))


# Create your views here.

def createTournament(request):
    games = GameCreatorWorkspaceACL.objects.filter(user_id=request.user.id)
    gameList = []
    for game in games:
        gameList.append(Game.objects.get(id=game.game_id))
    return render(request, 'tournament/createTournament.html', {'games': gameList})


def tournamentCreation(request):
    given_datetime = request.POST['starttime']
    given_datetime = given_datetime.split('T')
    givendate = (given_datetime[0]).split('-')
    giventime = (given_datetime[1]).split(':')
    start_time = datetime(int(givendate[0]), int(givendate[1]), int(givendate[2]), int(giventime[0]), int(giventime[1]),
                          0, 0)
    given_datetime = request.POST['endtime']
    given_datetime = given_datetime.split('T')
    givendate = (given_datetime[0]).split('-')
    giventime = (given_datetime[1]).split(':')
    end_time = datetime(int(givendate[0]), int(givendate[1]), int(givendate[2]), int(giventime[0]), int(giventime[1]),
                        0, 0)
    game_id = request.POST['game']
    game = Game.objects.get(id=int(game_id))
    tournament = TournamentInfo(name=request.POST['tournamentname'], game_id=game, startTime=start_time,
                                endTime=end_time, description=request.POST['description'])
    tournament.save()
    tournament = TournamentInfo.objects.latest('id')
    user = User.objects.get(id=request.user.id)
    tournamentCreator = TournamentCreatorWorkspaceACL(user=user, tournament=tournament)
    tournamentCreator.save()
    return baseTab(request, tournament.id)


def baseTab(request, tournament_id):
    # tournament_id = request.POST['tournamentid']
    # tournament_id = 9
    tournament = TournamentInfo.objects.get(id=int(tournament_id))
    game = Game.objects.get(id=tournament.game_id_id)
    visible = True
    registered = False
    print(request.user.id)
    if request.user.id is not None:
        if TournamentCreatorWorkspaceACL.objects.filter(user_id=request.user.id, tournament_id=tournament_id).exists():
            visible = False
        else:
            if TournamentParticipantWorkspaceACL.objects.filter(user_id=request.user.id,
                                                                tournament_id=tournament_id).exists():
                registered = True
    else:
        visible = False
    return render(request, 'tournament/baseTab.html',
                  {'tournament': tournament, 'game': game.game_title, 'visible': visible, 'registered': registered})


def reg_unreg(request):
    val = request.POST['register']
    val = val.split()
    if val[0] == 'reg':
        tournament = TournamentInfo.objects.get(id=val[1])
        user = User.objects.get(id=request.user.id)
        tournamentParticipant = TournamentParticipantWorkspaceACL(user=user, tournament=tournament)
        tournamentParticipant.save()
    else:
        tournamentParticipant = TournamentParticipantWorkspaceACL.objects.get(user_id=request.user.id,
                                                                              tournament_id=int(val[1]))
        tournamentParticipant.delete()
    return baseTab(request, int(val[1]))


def tournamentList(request):
    tournaments = TournamentInfo.objects.all()
    show = False
    if request.user.id is not None:
        show = True
    return render(request, 'tournament/tournamentList.html', {'tournaments': tournaments, 'show': show})
