from django.contrib import admin

# Register your models here.
from submission.models import Submission, WorkspaceTestSubmissionEntry

admin.site.register(Submission)
admin.site.register(WorkspaceTestSubmissionEntry)