from django.urls import path
from .dashboard import DashboardView
from .market import MarketDataSyncView

app_name = "jackietrade"

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("syncdata/", MarketDataSyncView.as_view(), name="syncdata"),
]
