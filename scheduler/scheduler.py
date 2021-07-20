import schedule
import time

from tournament.models import Tournament


def job():
    print("I'm working...")

def job2():
    print("I'm eating...")





def run():
    tournaments = Tournament.objects.all()
    tournament_phases = Tournament.TournamentPhase.names

    for tournament in tournaments:
        if (not tournament.shouldHaveStarted and
            tournament.phase == tournament.TournamentPhase.OPEN_FOR_REGISTRATION):
            print(tournament.name + "Should start at" + tournament.start_time)

        if (not tournament.shouldHaveEnded and
                tournament.phase == tournament.TournamentPhase.OPEN_FOR_SUBMISSION):
            print(tournament.name + "Should end at" + tournament.end_time)

    while True:
        schedule.run_pending()
        time.sleep(1)

