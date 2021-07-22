from django.db import models

# Create your models here.
import Online_AI.settings
from judge_queue.judge_queue import JudgeQueue


class JudgeQueueModels:
    judge_queue = JudgeQueue(max_workers=Online_AI.settings.MAX_TEST_GENERATION_LIMIT)