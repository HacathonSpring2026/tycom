from django.contrib import admin
from .models import (
    Category,
    Question,
    Random_name,
    Accuracy,
    Command,
    Extension,
    Score,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name", "created_at", "updated_at")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "question",
        "command",
        "description",
        "answer",
        "created_at",
        "updated_at",
    )


@admin.register(Random_name)
class Random_nameAdmin(admin.ModelAdmin):
    list_display = ("id", "random_name", "created_at", "updated_at")


@admin.register(Accuracy)
class AccuracyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "command",
        "challenge_count",
        "correct_count",
        "created_at",
        "updated_at",
    )


@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "category",
        "command",
        "target_type",
        "created_at",
        "updated_at",
    )


@admin.register(Extension)
class ExtensionAdmin(admin.ModelAdmin):
    list_display = ("id", "extension", "created_at", "updated_at")


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "score",
        "user",
        "category",
        "created_at",
        "updated_at",
    )
