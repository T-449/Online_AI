import random

import Online_AI.settings
from judge_queue.judge_queue import JudgeQueue
from match.models import Match
from submission.models import TournamentSubmissionEntry, Submission


class RoundRobinMatchGenerator:
    def __init__(self, tournament, judge_queue=JudgeQueue(Online_AI.settings.JUDGE_QUEUE_WORKER_COUNT)):
        self.tournament = tournament
        self.judge_queue = judge_queue

    def run(self):
        tournament_submissions = TournamentSubmissionEntry.objects.filter(tournament=self.tournament)
        submissions = list(tournament_submissions.values_list('submission', flat=True))
        users = tournament_submissions.values_list('submission__user', flat=True).distinct()

        print(submissions)
        print(users)

        final_submissions = []
        for user in users:
            s = Submission.objects.filter(user=user, pk__in=submissions).order_by('-submission_time')[0]
            final_submissions.append(s)

        for i in range(len(final_submissions)):
            for j in range(i + 1, len(final_submissions)):
                submission0 = final_submissions[i]
                submission1 = final_submissions[j]

                k = random.randint(0, 1)
                if k == 1:
                    temp = submission0
                    submission0 = submission1
                    submission1 = temp

                match = Match.objects.create_tournament_match(submission0=submission0, submission1=submission1,
                                                              tournament=self.tournament)
                self.judge_queue.submit(match)
                print(match)
        self.judge_queue.shutdown()
