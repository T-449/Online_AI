from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:match_uuid>', views.show_match_history, name='show_match_history'),
    path('judge/<uuid:match_uuid>', views.judge_match, name='judge_match'),
    path('delete/<uuid:match_uuid>', views.delete_match, name='delete_match'),
    path('history/<uuid:match_uuid>', views.dump_match_history, name='dump_history'),

]
