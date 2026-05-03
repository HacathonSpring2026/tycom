from django.conf import settings
from django.db import models


class Categories(models.Model):
    category_name = models.CharField(verbose_name="カテゴリー名", max_length=15)
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    class Meta:
        verbose_name_plural = "Category"

    def __str__(self):
        return self.category_name


class Commands(models.Model):
    TARGET_TYPE_CHOICES = [
        ("file", "ファイル"),
        ("directory", "ディレクトリ"),
        ("none", "なし"),
    ]
    category_id = models.ForeignKey(
        Categories, verbose_name="カテゴリーID", on_delete=models.CASCADE
    )
    command = models.CharField(verbose_name="コマンド", max_length=50)
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)
    target_type = models.CharField(
        verbose_name="タイプ判別",
        max_length=15,
        choices=TARGET_TYPE_CHOICES,
        default="none",
    )

    class Meta:
        verbose_name_plural = "command"

    def __str__(self):
        return self.command


class Questions(models.Model):
    question = models.TextField(verbose_name="問題文")
    command_id = models.ForeignKey(
        Commands, verbose_name="コマンドID", on_delete=models.CASCADE
    )
    description = models.TextField(verbose_name="説明文")
    answer = models.CharField(verbose_name="答え", max_length=100)
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    class Meta:
        verbose_name_plural = "Question"

    def __str__(self):
        return self.question


class Random_names(models.Model):
    random_name = models.CharField(verbose_name="ランダム名", max_length=50)
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    class Meta:
        verbose_name_plural = "Random_name"

    def __str__(self):
        return self.random_name


class Accuracies(models.Model):
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="ユーザーID", on_delete=models.CASCADE
    )
    command_id = models.ForeignKey(
        Commands, verbose_name="コマンドID", on_delete=models.CASCADE
    )
    accuracy_rate = models.FloatField(verbose_name="正解率")
    challenge_count = models.PositiveIntegerField(verbose_name="挑戦回数")
    correct_count = models.PositiveIntegerField(verbose_name="正解回数")
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    class Meta:
        verbose_name_plural = "accuracy"

    def __str__(self):
        return str(self.accuracy_rate)


class Extensions(models.Model):
    extension = models.CharField(verbose_name="拡張子", max_length=10)
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    class Meta:
        verbose_name_plural = "extension"

    def __str__(self):
        return self.extension


class Scores(models.Model):
    score = models.PositiveIntegerField(verbose_name="スコア")
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="ユーザーID", on_delete=models.CASCADE
    )
    category_id = models.ForeignKey(
        Categories, verbose_name="カテゴリーID", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    class Meta:
        verbose_name_plural = "score"

    def __str__(self):
        return self.score
