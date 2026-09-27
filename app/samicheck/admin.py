from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import TextField
from django.forms.widgets import Textarea

from .models import SamiCategory, SamiDay, SamiEntry, SamiIndicator


class SamiIndicatorInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        if any(self.errors):
            return

        total = 0

        for form in self.forms:
            if (
                form.cleaned_data
                and not form.cleaned_data.get("DELETE", False)
                and (form.instance.pk or form.has_changed())
            ):
                total += form.cleaned_data.get("max_level", 0) or 0

        if total > self.instance.max_score:
            raise ValidationError(
                f"Les niveaux maximum ({total}) "
                f"dépasse le score maximum de la catégorie "
                f"({self.instance.max_score})."
            )


class SamiIndicatorInline(admin.TabularInline):
    model: type[SamiIndicator] = SamiIndicator
    formset: type[SamiIndicatorInlineFormSet] = SamiIndicatorInlineFormSet
    extra = 1

    fields = (
        "title",
        "max_level",
        "description",
    )

    formfield_overrides: dict[type[TextField], dict[str, Textarea]] = {
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
        "total_score",
        "category_scores",
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
