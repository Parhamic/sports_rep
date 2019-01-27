from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from accounts.authentication import CheckConfirmed

urlpatterns = [
    path('', views.main_view, name='main_view'),
    path('news/<slug:slug>', views.PostDetailView.as_view(), name='post_view'),
    path('games/<int:pk>', views.GameDetailView.as_view(), name='game_view'),
    path('teams/<slug:slug>', views.TeamDetailView.as_view(), name='team_view'),
    path('players/<slug:slug>', views.PlayerDetailView.as_view(), name='player_view'),
    path('league/<int:pk>',
         views.LeagueDetailView.as_view(), name='league_view'),
    path('leagues/', views.LeaguesListView.as_view(), name='leagues_view'),

    # registration
    path('activate/<str:uidb64>/<str:token>',
         views.activate, name='activate'),
    path('register/', views.register_view, name='register'),
    path('reset_password/', views.reset_password_view, name='reset_password'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(
        template_name='signin.html', authentication_form=CheckConfirmed), name='login'),
]
