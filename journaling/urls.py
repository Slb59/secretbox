from django.urls import path

from .views import MemoCreateView
from .views import MemoDeleteView, MemoUnDeleteView
from .views import MemoUpdateView
from .utils import (
    check_memo_state,
    memo_mark_done,
)

app_name = "journaling"

urlpatterns = [
    path("add/", MemoCreateView.as_view(), name="add_memo"),
    path("edit/<int:pk>/", MemoUpdateView.as_view(), name="edit_memo"),
    path("delete/<int:pk>/", MemoDeleteView.as_view(), name="delete_memo"),
    path("undelete/<int:pk>/", MemoUnDeleteView.as_view(), name="undelete_todo"),
    path("todo/<int:pk>/check_state/", check_memo_state, name="check_memo_state"),
    path("todo/<int:pk>/done/", memo_mark_done, name="mark_done"),
]
