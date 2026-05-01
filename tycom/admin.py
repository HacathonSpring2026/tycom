from django.contrib import admin
from .models import (
    Categories,
    Questions,
    Random_names,
    Accuracies,
    Commands,
    Extensions,
    Scores,
)


@admin.register(Categories)
class Categoriesagdmin(admin.ModelAdmin):
    list_display = ("id", "category_name", "created_at", "updated_at")


@admin.register(Questions)
class Questionsagdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "question",
        "command_id",
        "description",
        "answer",
        "created_at",
        "updated_at",
    )


@admin.register(Random_names)
class Random_namesagdmin(admin.ModelAdmin):
    list_display = ("id", "random_name", "created_at", "updated_at")


@admin.register(Accuracies)
class Accuraciesagdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "command_id",
        "accuracy_rate",
        "challenge_count",
        "correct_count",
        "created_at",
        "updated_at",
    )


@admin.register(Commands)
class Commandsagdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "category_id",
        "command",
        "target_type",
        "created_at",
        "updated_at",
    )


@admin.register(Extensions)
class Extensionsagdmin(admin.ModelAdmin):
    list_display = ("id", "extension", "created_at", "updated_at")


@admin.register(Scores)
class Scoresagdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "score",
        "user_id",
        "category_id",
        "created_at",
        "updated_at",
    )
