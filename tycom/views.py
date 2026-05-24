from django.views import View
from .models import Category, Command, Question, Random_name, Extension
from django.shortcuts import redirect, render
import random
import json
from django.urls import reverse
from urllib.parse import urlencode
from django.http import HttpResponse


class StageSelectView(View):
    def get(self, request):
        category_list = Category.objects.all()  # HTMLに渡すためにカテゴリーテーブルのデータを全てcategory_listに入れる
        return render(request, "top.html", {"category_list": category_list})  # category_listという名前でHTMLに渡す

    def post(self, request):
        category_id = request.POST.get("category_id")  # HTMLからカテゴリIDをもらい変数へ入れる
        mode = request.POST.get("mode")
        request.session["category_id"] = category_id  # セッションへ['category_id']という名前で保存
        query = urlencode({"mode": mode})
        return redirect(f"{reverse('tycom:game_play')}?{query}")  # 保存まで完了したらgame_playへ飛ぶ


class GamePlayView(View):
    def get(self, request):
        category_id = request.session["category_id"]  # セッションに保存されたカテゴリーの取得
        commands = list(Command.objects.filter(category_id=category_id))  # 取得したカテゴリーのコマンドをリストで取得
        question_data = []

        for _ in range(100):
            command = random.choice(commands)  # コマンドのリストからランダムにチョイスする
            question = Question.objects.get(command_id=command.id)  # チョイスしたコマンドから問題を取得

            item = {  # 辞書型で１問分を纏める
                "question_id": question.id,
                "question": question.question,
                "description": question.description,
                "answer": question.answer,
            }

            if command.target_type == "directory":  # target_typeがdirectoryなら辞書にdirectory_nameのキーを作りランダム名を入れる
                directory_name = Random_name.objects.order_by("?").first()
                item["directory_name"] = directory_name.random_name
            elif command.target_type == "file":  # target_typeがfileならfile_nameのキーを作りランダム名と拡張子を合わせて入れる
                random_name = Random_name.objects.order_by("?").first()
                random_extension = Extension.objects.order_by("?").first()
                item["file_name"] = random_name.random_name + random_extension.extension

            question_data.append(item)

        return render(
            request,
            "game_play.html",
            {"question_data": json.dumps(question_data)},  # json文字列に変換
        )


class GameTimeEndView(View):
    def post(self, request):
        return HttpResponse("時間切れ")


class GameResultView(View):
    def get(self, request):
        return HttpResponse("結果表示")
