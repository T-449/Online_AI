import sys
import threading

import schedule
import time

from django.utils import timezone
from tendo.singleton import SingleInstanceException

from Online_AI.settings import ERROR_MARGIN_SECS
from judge_queue.judge_queue import JudgeQueue
from match_generator.round_robin_match_generator import RoundRobinMatchGenerator
from ranklist.victory_count_rank_generator import VictoryCountRankGenerator
from scheduler.models import get_need_to_reload_flag, set_need_to_reload_flag
from submission.models import Submission, TournamentSubmissionEntry
from tournament.models import Tournament
from tendo import singleton


def autoOpenSubmission(tournament):
    currentTime = timezone.now()
    sys.stdout.write("Opening Subs " + tournament.name + " at " + str(currentTime) + "\n")
    sys.stdout.flush()

    print(tournament.phase)
    if tournament.phase == tournament.TournamentPhase.OPEN_FOR_REGISTRATION:
        time_difference = tournament.start_time - currentTime

        if abs(time_difference.total_seconds()) <= ERROR_MARGIN_SECS:
            tournament.phase = tournament.TournamentPhase.OPEN_FOR_SUBMISSION
            tournament.save()
            return schedule.CancelJob


def execute_match_and_run(tournament):
    tournament.phase = Tournament.TournamentPhase.MATCH_EXECUTION
    tournament.save()

    match_generator = None
    if tournament.tournament_type == Tournament.TournamentType.ROUND_ROBIN:
        match_generator = RoundRobinMatchGenerator(tournament,JudgeQueue())
    match_generator.run()

    ranklist_generator = VictoryCountRankGenerator(tournament)
    ranklist_generator.generate_ranklist()

    submissions = TournamentSubmissionEntry.objects.filter(tournament=tournament)
    for s in submissions:
        s.submission.submission_visibility = Submission.SubmissionVisibility.PUBLIC
        s.submission.save()

    tournament.phase = Tournament.TournamentPhase.TOURNAMENT_ENDED
    print("Finished Running Tournament ", tournament)
    tournament.save()

def autoCloseSubmission(tournament):
    currentTime = timezone.now()
    sys.stdout.write("Closing Subs " + tournament.name + " at " + str(currentTime) + "\n")
    sys.stdout.flush()

    if tournament.phase == tournament.TournamentPhase.OPEN_FOR_SUBMISSION:
        time_difference = tournament.end_time - currentTime
        if abs(time_difference.total_seconds()) <= ERROR_MARGIN_SECS:
            tournament.phase = tournament.TournamentPhase.MATCH_EXECUTION
            tournament.save()

            thread = threading.Thread(target=execute_match_and_run, args=(tournament,))
            thread.start()

            return schedule.CancelJob


class Scheduler(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def reload_jobs(self):
        sys.stdout.write("Loading Jobs at " + str(timezone.now()) + "\n")
        sys.stdout.flush()

        schedule.clear()
        tournaments = Tournament.objects.all()
        for tournament in tournaments:
            if (not tournament.shouldHaveStarted):
                starttime = str(timezone.localtime(tournament.start_time).time())
                schedule.every().day.at(starttime).do(autoOpenSubmission, tournament=tournament)
                sys.stdout.write(tournament.name + " Scheduled to start at " + str(starttime) + "\n")
                sys.stdout.flush()

            if (not tournament.shouldHaveEnded):
                endtime = str(timezone.localtime(tournament.end_time).time())
                schedule.every().day.at(endtime).do(autoCloseSubmission, tournament=tournament)
                sys.stdout.write(tournament.name + " Scheduled to end at " + str(endtime) + "\n")
                sys.stdout.flush()

    def run(self):
        try:
            lock = singleton.SingleInstance()
        except SingleInstanceException as e:
            return

        sys.stdout.write("Scheduler Started.\n")

        while True:
            if get_need_to_reload_flag():
                self.reload_jobs()
                set_need_to_reload_flag(False)

            schedule.run_pending()
            time.sleep(1)
