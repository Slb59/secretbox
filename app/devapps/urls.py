from django.urls import path

from .views import (
    DevappsActionAPIView,
    DevappsDashboardView,
)

app_name = "devapps"

urlpatterns = [
    path("", DevappsDashboardView.as_view(), name="dashboard"),
    path("api/actions/", DevappsActionAPIView.as_view(), name="actions_api"),
]
