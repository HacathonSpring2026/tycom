from django.test import TestCase
from django.urls import reverse
from .models import Category


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
