from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:workspace_id>', views.show_workspace_home, name='game_creator_show_workspace'),
    path('<uuid:workspace_id>/post/description', views.post_game_description, name='game_creator_post_description'),
    path('<uuid:workspace_id>/post/judge_code', views.post_judge_code, name='game_creator_post_judge_code'),
    path('<uuid:workspace_id>/post/visualization_code', views.post_visualization_code,
         name='game_creator_post_visualization_code'),
    path('<uuid:workspace_id>/post/add_agent', views.post_add_agent,
         name='game_creator_post_add_agent'),
    path('<uuid:workspace_id>/post/create_match', views.post_create_match,
         name='game_creator_post_create_match'),
    path('<uuid:game_uuid>/raw/description/', views.get_game_description, name='game_creator_get_game_description'),
    path('<uuid:game_uuid>/raw/judge_code/', views.get_game_judge_code, name='game_creator_get_game_judge_code'),
    path('<uuid:game_uuid>/raw/visualization_code/', views.get_game_visualization_code,
         name='game_creator_get_game_visualization_code'),
    path('<uuid:workspace_id>/send_invite', views.send_invite,
         name='game_creator_send_workspace_invite'),
    path('<uuid:workspace_id>/post/update_test_agents', views.update_workspace_test_agents,
         name='game_creator_post_update_test_agents'),
]
