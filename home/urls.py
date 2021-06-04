from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('login', views.login, name='login'),
    path('createuser', views.createuser, name='createuser'),
    path('showprofile', views.showprofile, name='showprofile'),
    path('usercreation', views.usercreation, name='usercreation')
]