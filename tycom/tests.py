from django.test import TestCase
from django.urls import reverse
import json
from .models import Category, Command, Question, Random_name, Extension, Accuracy


class StageSelectViewTest(TestCase):
    def setUp(self):
        # テスト用カテゴリーを2つ作成
        self.category1 = Category.objects.create(category_name="Git")
        self.category2 = Category.objects.create(category_name="Docker")

    # --- GETのテスト ---

    def test_ページが開ける(self):
        response = self.client.get(reverse("tycom:stage_select"))
        self.assertEqual(response.status_code, 200)

    def test_カテゴリー一覧がHTMLに渡されている(self):
        response = self.client.get(reverse("tycom:stage_select"))
        # category_listというキーでcontextに入っているか
        self.assertIn("category_list", response.context)

    def test_カテゴリーが画面に表示される(self):
        response = self.client.get(reverse("tycom:stage_select"))
        self.assertContains(response, "Git")
        self.assertContains(response, "Docker")

    # --- POSTのテスト ---

    def test_カテゴリーIDがセッションに保存される(self):
        self.client.post(
            reverse("tycom:stage_select"), {"category_id": self.category1.id}
        )
        # セッションに保存されているか（POSTから来るので文字列になる）
        self.assertEqual(self.client.session["category_id"], str(self.category1.id))

    def test_POST後にgame_playへリダイレクトされる(self):
        response = self.client.post(
            reverse("tycom:stage_select"), {"category_id": self.category1.id}
        )
        self.assertEqual(response.status_code, 302)


class GamePlayViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(category_name="Git")
        self.command = Command.objects.create(
            command="git init",
            target_type="directory",
            category_id=self.category.id,
        )
        self.question = Question.objects.create(
            question="リポジトリを初期化するコマンドは？",
            command_id=self.command.id,
            description="説明",
            answer="git init",
        )
        self.random_name = Random_name.objects.create(random_name="myproject")
        self.extension = Extension.objects.create(extension=".py")
        # セッションにカテゴリーIDを保存
        session = self.client.session
        session["category_id"] = str(self.category.id)
        session.save()

    def test_ページが開ける(self):
        response = self.client.get(reverse("tycom:game_play"))
        self.assertEqual(response.status_code, 200)

    def test_questionがHTMLに渡される(self):
        response = self.client.get(reverse("tycom:game_play"))
        self.assertIn("question_data", response.context)


from django.contrib.auth import get_user_model

User = get_user_model()


class GameTimeEndViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass")
        self.client.force_login(self.user)
        self.category = Category.objects.create(category_name="Git")
        self.command = Command.objects.create(
            command="git status",
            target_type="none",
            category_id=self.category.id,
        )
        self.question = Question.objects.create(
            question="状態確認コマンドは？",
            command_id=self.command.id,
            description="説明",
            answer="git status",
        )

    def test_POST後にgame_resultへリダイレクトされる(self):
        data = {"results": []}
        response = self.client.post(
            reverse("tycom:game_time_end"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 302)

    def test_POSTでAccuracyが保存される(self):
        data = {
            "results": [
                {
                    "question_id": self.question.id,
                    "typed_chars": 10,
                    "challenge_count": 2,
                }
            ]
        }
        self.client.post(
            reverse("tycom:game_time_end"),
            data=json.dumps(data),
            content_type="application/json",
        )
        accuracy = Accuracy.objects.get(user=self.user, command=self.command)
        self.assertEqual(accuracy.challenge_count, 2)

    def test_resultsがセッションに保存される(self):
        results = [
            {"question_id": self.question.id, "typed_chars": 10, "challenge_count": 1}
        ]
        self.client.post(
            reverse("tycom:game_time_end"),
            data=json.dumps({"results": results}),
            content_type="application/json",
        )
        self.assertEqual(self.client.session["results"], results)


class GameResultViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(category_name="Git")
        self.command = Command.objects.create(
            command="git status",
            target_type="none",
            category_id=self.category.id,
        )
        self.question = Question.objects.create(
            question="状態確認コマンドは？",
            command_id=self.command.id,
            description="説明",
            answer="git status",
        )

    def test_ページが開ける(self):
        response = self.client.get(reverse("tycom:game_result"))
        self.assertEqual(response.status_code, 200)

    def test_result_listがHTMLに渡される(self):
        session = self.client.session
        session["results"] = [{"question_id": self.question.id, "challenge_count": 1}]
        session.save()
        response = self.client.get(reverse("tycom:game_result"))
        self.assertIn("result_list", response.context)

    def test_コマンドと説明が渡される(self):
        session = self.client.session
        session["results"] = [{"question_id": self.question.id, "challenge_count": 1}]
        session.save()
        response = self.client.get(reverse("tycom:game_result"))
        result_list = response.context["result_list"]
        self.assertEqual(result_list[0]["command"], "git status")
        self.assertEqual(result_list[0]["description"], "説明")
