from django.urls import path

from .views import SamicheckDashboardView

app_name = "samicheck"

urlpatterns = [
    path("", SamicheckDashboardView.as_view(), name="dashboard"),
]
