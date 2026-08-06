from django.contrib import admin

from .models import (
    DictavoixDictionaryWord,
    DictavoixExercise,
    DictavoixSession,
    DictavoixTheme,
)


@admin.register(DictavoixTheme)
class DictavoixThemeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(DictavoixDictionaryWord)
class DictavoixDictionaryWordAdmin(admin.ModelAdmin):
    list_display = ("word", "theme")
    list_filter = ("theme",)
    search_fields = ("word",)


@admin.register(DictavoixExercise)
class DictavoixExerciseAdmin(admin.ModelAdmin):
    list_display = ("title", "theme", "created_by", "created_at")
    list_filter = ("theme",)
    search_fields = ("title", "text")


@admin.register(DictavoixSession)
class DictavoixSessionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "exercise",
        "started_at",
        "finished_at",
        "error_count",
        "total_word_count",
        "dictionary_word_count",
    )
    list_filter = ("exercise", "user")
    search_fields = ("user__email", "exercise__title")
