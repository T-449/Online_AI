import os
import shutil

THREE_WAY_PATH = "matchExecutionUnit/three-way.out"
RUNNER_PATH = "matchExecutionUnit/runner.sh"
SANDBOX = 'Sandbox/'

def execute_match(match, dir=SANDBOX):
    submission0_filepath = match.submission0.get_submission_filepath()
    submission1_filepath = match.submission1.get_submission_filepath()
    judge_code_filepath = match.game.get_game_judge_code_filepath()

    os.makedirs(dir, exist_ok=True)
    os.makedirs(dir + "/zero", exist_ok=True)
    os.makedirs(dir + "/one", exist_ok=True)
    os.makedirs(dir + "/judge", exist_ok=True)

    shutil.copy(THREE_WAY_PATH, dir + "/three-way.out")
    shutil.copy(RUNNER_PATH, dir + "/runner.sh")
    shutil.copy(submission0_filepath, dir + '/zero/zero')
    shutil.copy(submission1_filepath, dir + '/one/one')
    shutil.copy(judge_code_filepath, dir + '/judge/judge')
    print("cd " + dir + "; ./three-way.out " + match.submission0.submission_language + " ./zero/zero "
              + match.submission1.submission_language + " ./one/one "
              + match.game.game_judge_code_language + " ./judge/judge")
    os.system("cd " + dir + "; ./three-way.out " + match.submission0.submission_language + " ./zero/zero "
              + match.submission1.submission_language + " ./one/one "
              + match.game.game_judge_code_language + " ./judge/judge")
    shutil.copy(dir + "/matchhistory.json", match.history_filepath)
    shutil.rmtree(dir)

# from matchExecutionUnit import matchExecutionUnit
# from match import models
# m=models.Match.objects.get(pk=2)
# matchExecutionUnit.execute_match(m,"testdir2")
