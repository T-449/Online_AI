import os
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Process

from matchExecutionUnit.matchExecutionUnit import execute_match


def execute_submitted_match(match):
    sandbox_id = str(os.getpid())
    print("**************",sandbox_id," ###########")
    p = Process(target=execute_match, args=(match,"sandbox"+sandbox_id))
    p.start()
    p.join()


class JudgeQueue:

    def __init__(self, max_workers=3):
        self.executor = ProcessPoolExecutor(max_workers=max_workers)

    def submit(self, match):
        print("Inside submit")
        t = self.executor.submit(execute_submitted_match,match)
        print(self.executor)

MAX_TEST_GENERATION_LIMIT = 3

class GlobalJudgeQueue:
    judge_queue = JudgeQueue(max_workers=MAX_TEST_GENERATION_LIMIT)
