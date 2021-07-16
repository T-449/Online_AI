from django.urls import path
from . import views

urlpatterns = [
    path('create', views.show_tournament_creator_page, name='show_tournament_creator_page'),
    path('post/create_tournament', views.create_tournament, name='post_create_tournament'),
    path('<uuid:tournament_uuid>', views.show_tournament_workspace, name='show_tournament_workspace'),
    path('<uuid:tournament_uuid>/register', views.reg_unreg, name='register_tournament'),
    path('tournamentList', views.tournamentList, name='tournamentList'),
]