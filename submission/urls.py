from django.urls import path
from . import views

urlpatterns = [
    path('raw/<uuid:submission_uuid>', views.show_raw_submission, name='show_raw_submission')
]
