from django.db import models


# Create your models here.

class JobStatus(models.Model):
    name = models.CharField(max_length=256, default='JobStatus', primary_key=True)
    need_to_reload_jobs = models.BooleanField(default=True)


def getJobStatus():
    try:
        jobstatus = JobStatus.objects.get(name='JobStatus')
        return jobstatus
    except JobStatus.DoesNotExist:
        jobstatus = JobStatus.objects.create(name='JobStatus', need_to_reload_jobs=True)
        jobstatus.save()
        return jobstatus

def set_need_to_reload_flag(value):
    jobstatus = getJobStatus()
    jobstatus.need_to_reload_jobs = value
    jobstatus.save()

def get_need_to_reload_flag():
    return getJobStatus().need_to_reload_jobs