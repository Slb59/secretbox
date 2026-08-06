from django.urls import path

from .views import DictavoixDashboardView, ExerciseDetailView

app_name = "dictavoix"

urlpatterns = [
    path("", DictavoixDashboardView.as_view(), name="dashboard"),
    path("exercise/<int:pk>/", ExerciseDetailView.as_view(), name="exercise_detail"),
]
