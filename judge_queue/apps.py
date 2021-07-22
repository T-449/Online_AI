import sys

from django.apps import AppConfig

import Online_AI.settings


class JudgeQueueConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'judge_queue'

    #judge_queue = JudgeQueue(max_workers=Online_AI.settings.JUDGE_QUEUE_WORKER_COUNT)

