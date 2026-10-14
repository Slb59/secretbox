from django.urls import path

from .views import SamicheckDashboardView, create_day

app_name = "samicheck"

urlpatterns = [
    path("", SamicheckDashboardView.as_view(), name="dashboard"),
    path("days/", create_day, name="create_day"),
]
