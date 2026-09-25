from django import forms
from django.contrib import admin
from django.db import models

from .models import SamiCategory, SamiDay, SamiEntry, SamiIndicator


class SamiIndicatorInline(admin.TabularInline):
    model: type[SamiIndicator] = SamiIndicator
    extra = 1
    fields = (
        "title",
        "max_level",
        "description",
    )
    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(
                attrs={
                    "rows": 2,
                    "cols": 40,
                }
            ),
        },
    }
    ordering = ("title",)


@admin.register(SamiCategory)
class SamiCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "max_score",
    )
    search_fields = ("name",)
    ordering = ("name",)
    inlines: tuple[type[SamiIndicatorInline]] = (SamiIndicatorInline,)


@admin.register(SamiIndicator)
class SamiIndicatorAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "max_level",
    )
    list_filter = ("category",)
    search_fields = (
        "title",
        "description",
    )
    ordering = (
        "category",
        "title",
    )
    list_select_related = ("category",)


@admin.register(SamiDay)
class SamiDayAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "started_at",
        "ended_at",
    )
    date_hierarchy = "date"
    ordering = ("-date",)


@admin.register(SamiEntry)
class SamiEntryAdmin(admin.ModelAdmin):
    list_display = (
        "day",
        "indicator",
        "value",
        "note",
    )
    list_filter = ("day", "indicator__category")
    search_fields = (
        "value",
        "indicator__title",
        "indicator__description",
    )
    ordering = (
        "-day",
        "indicator__category",
        "indicator",
    )
    list_select_related = ("day", "indicator", "indicator__category")
