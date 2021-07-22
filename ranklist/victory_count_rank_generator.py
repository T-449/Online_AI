from match.models import TournamentMatchTable
from ranklist.models import Ranklist


class VictoryCountRankGenerator:
    def __init__(self, tournament):
        self.tournament = tournament

    def generate_ranklist(self):
        tournament_matches = TournamentMatchTable.objects.filter(tournament=self.tournament)
        rank_count = {}
        for tournament_match_entry in tournament_matches:
            match = tournament_match_entry.match

            if match.submission0 not in rank_count:
                rank_count[match.submission0] = 0

            if match.submission1 not in rank_count:
                rank_count[match.submission1] = 0

            if match.match_results is not None:
                if match.match_results.lower() == "not decided":
                    match_result = "Not Decided"
                elif match.match_results.lower() == "win":
                    rank_count[match.submission0] += 1
                elif self.match_results.lower() == "loss":
                    rank_count[match.submission1] += 1
                elif self.match_results.lower() == "draw":
                    match_result = "Game drawn"
                else:
                    match_result = "Error"
        print(rank_count)

        ranklist = dict(sorted(rank_count.items(), key=lambda item: -item[1]))

        index = 1
        Ranklist.objects.filter(tournament=self.tournament).delete()
        for rank_entry in ranklist:
            Ranklist.objects.create(tournament=self.tournament, submission=rank_entry, rank=index)
            index += 1
