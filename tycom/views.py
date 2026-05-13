from django.views import View
from .models import Category
from django.shortcuts import redirect, render


class StageSelectView(View):
    def get(self, request):
        category_list = (
            Category.objects.all()
        )  # HTMLに渡すためにカテゴリーテーブルのデータを全てcategory_listに入れる
        return render(
            request, "top.html", {"category_list": category_list}
        )  #:category_listと言うを変数をcategory_listという名前でHTMLに渡す

    def post(self, request):
        category_id = request.POST.get(
            "category_id"
        )  # HTMLからカテゴリIDをもらい変数へ入れる
        request.session["category_id"] = (
            category_id  # セッションへ['category_id']と言う名前で保存
        )
        return redirect("tycom:game_play")  # 保存まで完了したら['category_id']へ飛ぶ


class GamePlayView(View):
    def get(self, request):
        return HttpResponse("問題画面")


class GameTimeEndView(View):
    def post(self, request):
        return HttpResponse("時間切れ")


class GameResultView(View):
    def get(self, request):
        return HttpResponse("結果表示")
