from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from scheduler.models import set_need_to_reload_flag
from tournament.models import Tournament


@receiver(post_delete, sender=Tournament)
@receiver(post_save, sender=Tournament)
def clearJobsLoadedFlag(sender, instance, created, **kwargs):
    set_need_to_reload_flag(True)