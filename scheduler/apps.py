from threading import Thread

from django.apps import AppConfig


class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'

    def ready(self):
        from scheduler.scheduler import Scheduler
        thread = Scheduler("scheduler")
        thread.start()
