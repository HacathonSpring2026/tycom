from django.views import View
from .models import Category, Command, Question, Random_name, Extension
from django.shortcuts import redirect, render
import random


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
        category_id = request.session["category_id"]
        commands = list(Command.objects.filter(category_id=category_id))
        command = random.choice(commands)
        questions = list(Question.objects.filter(command_id=command.id))
        question = random.choice(questions)
        if command.target_type == "directory":
            directory_name = Random_name.objects.order_by("?").first()
            return render(
                request,
                "game_play.html",
                {"question": question, "directory_name": directory_name},
            )
        elif command.target_type == "file":
            random_name = Random_name.objects.order_by("?").first()
            random_extension = Extension.objects.order_by("?").first()
            file_name = random_name.random_name + random_extension.Extension
            return render(
                request,
                "game_play.html",
                {"question": question, "file_name": file_name},
            )


class GameTimeEndView(View):
    def post(self, request):
        return HttpResponse("時間切れ")


class GameResultView(View):
    def get(self, request):
        return HttpResponse("結果表示")
