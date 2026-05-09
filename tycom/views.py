from django.views import View
from django.http import HttpResponse


class StageSelectView(View):
    def get(self, request):
        return HttpResponse("ステージ選択画面")


class GamePlayView(View):
    def get(self, request):
        return HttpResponse("問題画面")


class GameTimeEndView(View):
    def post(self, request):
        return HttpResponse("時間切れ")


class GameResultView(View):
    def get(self, request):
        return HttpResponse("結果表示")
