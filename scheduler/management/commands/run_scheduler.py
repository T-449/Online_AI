from django.core.management.base import BaseCommand, CommandError

from scheduler import scheduler


class Command(BaseCommand):
    help = 'Starts the scheduler if not already running'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        scheduler.run_scheduler()
