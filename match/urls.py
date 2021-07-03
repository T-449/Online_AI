from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:match_uuid>', views.show_match_history, name='show_match_history'),
    path('judge/<uuid:match_uuid>', views.judge_match, name='judge_match'),
]
