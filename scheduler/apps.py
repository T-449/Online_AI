import sys
from threading import Thread
from django.apps import AppConfig


class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'

    def ready(self):
        if 'runserver' in sys.argv:
            from scheduler.scheduler import Scheduler
            import scheduler.signals
            from scheduler.models import set_need_to_reload_flag

            set_need_to_reload_flag(True)
            thread = Scheduler("scheduler")
            thread.start()
