from django.urls import path

from .views import (
    EscapeVaultCreateView,
    EscapeVaultDeleteView,
    EscapeVaultEditView,
    EscapeVaultListView,
    EscapeVaultMapView,
    EscapeVaultParametersView,
)

app_name = "escapevault"

urlpatterns = [
    path("map/", EscapeVaultMapView.as_view(), name="dashboard"),
    path("add/", EscapeVaultCreateView.as_view(), name="add_position"),
    path("list/", EscapeVaultListView.as_view(), name="list_positions"),
    path("<int:pk>/edit/", EscapeVaultEditView.as_view(), name="edit_position"),
    path("<int:pk>/delete/", EscapeVaultDeleteView.as_view(), name="delete_position"),
    path("parameters/", EscapeVaultParametersView.as_view(), name="parameters"),
]
