from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as user_views

urlpatterns = [

    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', user_views.register, name='register'),
    path('profile/<slug:profile_name>', user_views.view_profile, name='viewprofile'),
    path('update_profile/', user_views.update_profile, name='update_profile'),

]