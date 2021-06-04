from django.urls import path
from . import views

urlpatterns = [
    path('<int:workspace_id>/', views.show_workspace_home, name='game_creator_show_workspace')
]