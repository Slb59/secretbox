from django.urls import path

from .asset import AssetListView, AssetUpdateView
from .dashboard import DashboardView
from .market import MarketDataSyncView
from .watchlist import (
    WatchlistAddAssetView,
    WatchlistCreateView,
    WatchlistDeleteView,
    WatchlistListView,
    WatchlistUpdateView,
)

app_name = "jackietrade"

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("syncdata/", MarketDataSyncView.as_view(), name="syncdata"),
    path("watchlists/", WatchlistListView.as_view(), name="watchlist_list"),
    path("watchlists/new/", WatchlistCreateView.as_view(), name="watchlist_create"),
    path(
        "watchlists/<int:pk>/edit/",
        WatchlistUpdateView.as_view(),
        name="watchlist_update",
    ),
    path(
        "watchlists/<int:pk>/delete/",
        WatchlistDeleteView.as_view(),
        name="watchlist_delete",
    ),
    path(
        "watchlists/<int:pk>/add-asset/",
        WatchlistAddAssetView.as_view(),
        name="watchlist_add_asset",
    ),
    path("assets/", AssetListView.as_view(), name="asset_list"),
    path("assets/<int:pk>/edit/", AssetUpdateView.as_view(), name="asset_update"),
]
