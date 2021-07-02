import os
import shutil


def execute_match(match, dir):
    submission0_filepath = match.submission0.get_submission_filepath()
    submission1_filepath = match.submission1.get_submission_filepath()
    judge_code_filepath = match.game.get_game_judge_code_filepath()

    os.makedirs(dir, exist_ok=True)
    os.makedirs(dir + "/zero", exist_ok=True)
    os.makedirs(dir + "/one", exist_ok=True)
    os.makedirs(dir + "/judge", exist_ok=True)
    shutil.copy(submission0_filepath, dir + '/zero/')
    shutil.copy(submission1_filepath, dir + '/one/')
    shutil.copy(judge_code_filepath, dir + '/judge/')


# from matchExecutionUnit import matchExecutionUnit
# from match import models
# m=models.Match.objects.get(pk=2)
# matchExecutionUnit.execute_match(m,"testdir2")
