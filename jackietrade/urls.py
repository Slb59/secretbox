from django.urls import path
from .dashboard import DashboardView
from .market import MarketDataSyncView
from .watchlist import (
    WatchlistListView,
    WatchlistCreateView,
    WatchlistUpdateView,
    WatchlistDeleteView,
    ToggleAssetWatchlistView,
)

app_name = "jackietrade"

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("syncdata/", MarketDataSyncView.as_view(), name="syncdata"),

    path("watchlists/", WatchlistListView.as_view(), name="watchlist_list"),
    path("watchlists/new/", WatchlistCreateView.as_view(), name="watchlist_create"),
    path("watchlists/<int:pk>/edit/", WatchlistUpdateView.as_view(), name="watchlist_update"),
    path("watchlists/<int:pk>/delete/", WatchlistDeleteView.as_view(), name="watchlist_delete"),

    path("watchlists/<int:pk>/toggle-asset/", ToggleAssetWatchlistView.as_view(), name="toggle_asset"),

]
