from django.contrib import admin

from ..journal.journalmodels import TradeJournalEntry, TradeJournalScreenshot


class TradeJournalScreenshotInline(admin.TabularInline):
    model = TradeJournalScreenshot
    extra = 1


@admin.register(TradeJournalEntry)
class TradeJournalEntryAdmin(admin.ModelAdmin):
    list_display = (
        "session_date",
        "asset",
        "confidence_level",
        "planned_entry_price",
        "planned_stop_loss",
        "planned_take_profit",
        "exit_reason",
        "reviewed_at",
    )

    list_filter = (
        "session_date",
        "confidence_level",
        "exit_reason",
        "asset__sector",
    )

    search_fields = (
        "asset__symbol",
        "asset__name",
        "observation_notes",
        "market_context",
        "execution_notes",
        "result_notes",
    )

    autocomplete_fields = ("asset",)

    readonly_fields = (
        "created_at",
        "quantity_display",
        "invested_amount_display",
        "potential_profit_display",
        "potential_loss_display",
    )

    date_hierarchy = "session_date"

    inlines = [
        TradeJournalScreenshotInline,
    ]

    fieldsets = (
        (
            "Informations générales",
            {
                "fields": (
                    "asset",
                    "session_date",
                    "created_at",
                    "reviewed_at",
                )
            },
        ),
        (
            "Observations",
            {
                "fields": (
                    "observation_notes",
                    "market_context",
                )
            },
        ),
        (
            "Analyse",
            {
                "fields": (
                    "planned_entry_price",
                    "planned_stop_loss",
                    "planned_take_profit",
                    "confidence_level",
                    "quantity_display",
                    "invested_amount_display",
                    "potential_profit_display",
                    "potential_loss_display",
                )
            },
        ),
        (
            "Décision",
            {
                "fields": (
                    "execution_notes",
                    "entry_order_at",
                    "entry_quantity",
                    "entry_price_executed",
                )
            },
        ),
        (
            "Conclusion",
            {
                "fields": (
                    "result_notes",
                    "exit_order_at",
                    "exit_quantity",
                    "exit_price",
                    "exit_reason",
                )
            },
        ),
    )

    @admin.display(description="Quantité théorique")
    def quantity_display(self, obj):

        if not obj.pk:
            return "-"

        return obj.quantity

    @admin.display(description="Montant investi")
    def invested_amount_display(self, obj):

        if not obj.pk or not obj.entry_price:
            return "-"

        return f"{obj.invested_amount:.2f} €"

    @admin.display(description="Profit potentiel")
    def potential_profit_display(self, obj):

        if not obj.pk or not obj.entry_price or not obj.take_profit:
            return "-"

        return f"{obj.potential_profit:.2f} €"

    @admin.display(description="Perte potentielle")
    def potential_loss_display(self, obj):

        if not obj.pk or not obj.entry_price or not obj.stop_loss:
            return "-"

        return f"{obj.potential_loss:.2f} €"
