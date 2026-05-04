from django.urls import path
from . import views

app_name = "tycom"

urlpatterns = [
    path("stage-select/", views.StageSelectView.as_view(), name="stage_select"),
    path("game/play/", views.GamePlayView.as_view(), name="game_play"),
    path("game/time-end/", views.GameTimeEndView.as_view(), name="game_time_end"),
    path("game/result/", views.GameResultView.as_view(), name="game_result"),
]
