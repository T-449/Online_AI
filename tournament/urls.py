from django.urls import path
from . import views

urlpatterns = [
    path('', views.createTournament, name='createTournament'),
    path('tournamentCreation', views.tournamentCreation, name='tournamentCreation'),
    path('<int:tournament_id>basetab', views.baseTab, name='baseTab'),
    path('reg_unreg', views.reg_unreg, name='reg_unreg'),
    path('tournamentList', views.tournamentList, name='tournamentList'),
]