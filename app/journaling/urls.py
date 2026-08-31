from django.urls import path

from .utils import (
    check_memo_state,
    memo_mark_done,
)
from .views import (
    DashboardDataView,
    MemoCreateView,
    MemoDeleteView,
    MemoHistoryView,
    MemoReportView,
    MemoStartDayView,
    MemoUnDeleteView,
    MemoUpdateAPIView,
    MemoUpdateView,
    MemoValidateView,
)

app_name = "journaling"

urlpatterns = [
    path("add/", MemoCreateView.as_view(), name="add_memo"),
    path("edit/<int:pk>/", MemoUpdateView.as_view(), name="edit_memo"),
    path("delete/<int:pk>/", MemoDeleteView.as_view(), name="delete_memo"),
    path("undelete/<int:pk>/", MemoUnDeleteView.as_view(), name="undelete_memo"),
    path("todo/<int:pk>/check_state/", check_memo_state, name="check_memo_state"),
    path("todo/<int:pk>/done/", memo_mark_done, name="mark_done"),
    path("validate/<int:pk>/", MemoValidateView.as_view(), name="validate_memo"),
    path("report/<int:pk>/", MemoReportView.as_view(), name="report_memo"),
    path("history/<int:pk>/", MemoHistoryView.as_view(), name="history"),
    path("start-day/", MemoStartDayView.as_view(), name="start_day"),
    path("api/memos/", DashboardDataView.as_view(), name="memos_api"),
    path("api/memos/update/", MemoUpdateAPIView.as_view(), name="update_memo_api"),
]
