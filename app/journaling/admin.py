from django.contrib import admin

from .colors import ColorParameter
from .memo import Memo, MemoHistory


@admin.register(ColorParameter)
class ColorParameterAdmin(admin.ModelAdmin):
    list_display = ("priority", "periodic", "category", "place", "color")
    list_filter = ("priority", "periodic", "category", "place")
    search_fields = ("priority", "periodic", "category", "place", "color")
    ordering = ("priority", "periodic", "category", "place")


@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    list_display = (
        "description",
        "user",
        "state",
        "planned_date",
        "report_date",
        "done_date",
        "priority",
        "category",
        "place",
        "periodic",
        "process_today",
    )
    list_filter = (
        "state",
        "priority",
        "category",
        "place",
        "periodic",
        "process_today",
        "user",
    )
    search_fields = (
        "description",
        "note",
        "user__username",
        "user__email",
    )
    filter_horizontal = ("who",)
    date_hierarchy = "planned_date"
    ordering = ("-planned_date", "-timestamp")
    readonly_fields = ("timestamp", "original_planned_date")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "description",
                    "state",
                    "priority",
                    "category",
                    "place",
                    "periodic",
                    "process_today",
                )
            },
        ),
        (
            "Planning",
            {
                "fields": (
                    "planned_date",
                    "report_date",
                    "done_date",
                    "appointment",
                    "duration",
                    "timestamp",
                )
            },
        ),
        (
            "Assignation",
            {
                "fields": ("who",),
            },
        ),
        (
            "Notes",
            {
                "fields": ("note",),
            },
        ),
    )


@admin.register(MemoHistory)
class MemoHistoryAdmin(admin.ModelAdmin):
    list_display = ("memo", "changed_by", "action", "timestamp")
    list_filter = ("action", "changed_by", "memo__state")
    search_fields = (
        "memo__description",
        "changes",
        "changed_by__username",
        "changed_by__email",
    )
    readonly_fields = ("timestamp", "changes")
    date_hierarchy = "timestamp"
    ordering = ("-timestamp",)
