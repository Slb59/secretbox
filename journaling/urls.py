from django.urls import path

from .memoreateview import TodoCreateView
from .memodeleteview import MemoDeleteView, MemoUnDeleteView
from .memoreportview import TodoReportView
from .memoupdateview import TodoUpdateView
from .memovalidateview import TodoValidateView
from .memohistoryview import MemoHistoryView
from .dashbordstoptimerview import DashboardTimerView
from .utils import (
    check_memo_state,
    memo_mark_done,
)

app_name = "dashboard"

urlpatterns = [
    path("add/", TodoCreateView.as_view(), name="add_todo"),
    path("edit/<int:pk>/", TodoUpdateView.as_view(), name="edit_todo"),
    path("delete/<int:pk>/", MemoDeleteView.as_view(), name="delete_todo"),
    path("undelete/<int:pk>/", MemoUnDeleteView.as_view(), name="undelete_todo"),
    path("report/<int:pk>/", TodoReportView.as_view(), name="report_todo"),
    path("validate/<int:pk>/", TodoValidateView.as_view(), name="validate_todo"),
    path("todo/<int:pk>/check_state/", check_todo_state, name="check_todo_state"),
    path("todo/<int:pk>/done/", todo_mark_done, name="mark_done"),
    path("history/<int:pk>/", MemoHistoryView.as_view(), name="history"),
    path("stop_timer/", DashboardTimerView.as_view(), name="stop_timer"),
]
