from django.urls import path
from . import views


urlpatterns = [
    path('<uuid:workspace_id>', views.show_workspace_home, name='game_creator_show_workspace'),
    # path('<int:game_uid>/raw/description/', views.get_game_description, name='game_creator_get_game_description'),
    # path('<int:game_uid>/raw/judge_code/', views.get_game_judge_code, name='game_creator_show_workspace'),
]