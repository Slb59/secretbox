from django.urls import path

from .views import (
    DictavoixDashboardView,
    DictavoixDictionaryView,
    DictavoixDictionaryWordsAPIView,
    ExerciseDetailView,
)

app_name = "dictavoix"

urlpatterns = [
    path("", DictavoixDashboardView.as_view(), name="dashboard"),
    path(
        "dictionary/<int:theme_pk>/",
        DictavoixDictionaryView.as_view(),
        name="dictionary",
    ),
    path(
        "dictionary/<int:theme_pk>/api/",
        DictavoixDictionaryWordsAPIView.as_view(),
        name="dictionary_api",
    ),
    path("exercise/<int:pk>/", ExerciseDetailView.as_view(), name="exercise_detail"),
]
