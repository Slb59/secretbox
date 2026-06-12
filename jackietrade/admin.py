from django.contrib import admin


from .models import (
    Asset,
    Sector,
    Exchange,
    Watchlist,
    WatchlistItem,
    Candle,
)


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "code",
    )

    search_fields = (
        "name",
        "code",
    )

    class Media:
        css = {
            "all": ("css/admin.css",)
        }

@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "code",
        "country",
        "timezone",
    )

    search_fields = (
        "name",
        "code",
    )

    list_filter = (
        "country",
    )

class WatchlistItemInline(admin.TabularInline):

    model = WatchlistItem

    extra = 1

    autocomplete_fields = (
        "asset",
    )

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):

    list_display = (
        "symbol",
        "name",
        "asset_type",
        "sector",
        "exchange",
        "is_active",
        "last_sync_at",
    )

    search_fields = (
        "symbol",
        "name",
    )

    list_filter = (
        "asset_type",
        "sector",
        "exchange",
        "is_active",
    )

    autocomplete_fields = (
        "sector",
        "exchange",
    )

    inlines = [
        WatchlistItemInline,
    ]

    class Media:
        css = {
            "all": ("css/admin.css",)
        }

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "user",
        "is_default",
    )

    search_fields = (
        "name",
        "user__username",
    )

    inlines = [
        WatchlistItemInline,
    ]

@admin.register(Candle)
class CandleAdmin(admin.ModelAdmin):

    list_display = (
        "asset",
        "timeframe",
        "timestamp",
        "close",
        "volume",
    )

    list_filter = (
        "timeframe",
    )

    search_fields = (
        "asset__symbol",
    )

    autocomplete_fields = (
        "asset",
    )

    date_hierarchy = "timestamp"

    list_per_page = 100
