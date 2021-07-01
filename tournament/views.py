from django.shortcuts import render
import random
import string
from datetime import datetime

from game_creator.models import Game
from tournament.models import TournamentInfo


def generateRandomString(characters):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=characters))


# Create your views here.

def createTournament(request):
    games = Game.objects.all()
    return render(request, 'tournament/createTournament.html', {'games': games})


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
    return createTournament(request)


def baseTab(request):
    # tournament_id = request.POST['tournamentid']
    tournament_id = 1
    tournament = TournamentInfo.objects.get(id=int(tournament_id))
    game = Game.objects.get(id=tournament.game_id_id)
    return render(request, 'tournament/basetab.html', {'tournament': tournament, 'game': game.game_title})
