from django.urls import path
from . import views

urlpatterns = [
    path('showjobs', views.show_jobs, name='show_jobs'),
]