from django.urls import path
from . import views

urlpatterns = [
    path('', views.createTournament, name='createTournament'),
    path('tournamentCreation', views.tournamentCreation, name='tournamentCreation'),
    path('basetab', views.baseTab, name='baseTab'),
]