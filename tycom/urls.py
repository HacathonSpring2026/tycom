from django.urls import path
from . import views

app_name = "tycom"

urlpatterns = [
    path("login/", views.login_page, name="login_page"),
    path("signup/", views.signup_page, name="signup_page"),
    path("logout/", views.logout, name="logout"),
    path("stage_select/", views.stage_select, name="stage_select"),
    path("game/play/", views.game_play, name="game_play"),
    path("game/time_end/", views.game_time_end, name="game_time_end"),
    path("game/result/", views.game_result, name="game_result"),
]
