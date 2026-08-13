from django.urls import path

from .views import DocubaseAppListView, DocubaseDocumentView, DocubaseIndexView

app_name = "docubase"

urlpatterns = [
    # Main documentation index
    path("", DocubaseIndexView.as_view(), name="index"),
    # List documents for a specific app
    path("<str:app>/", DocubaseAppListView.as_view(), name="app_docs"),
    # Display a specific document
    path("<str:app>/<str:doc>/", DocubaseDocumentView.as_view(), name="document"),
]
