import logging

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET, require_POST

from .memohistorymodel import MemoHistory
from .memo import Memo

logger = logging.getLogger(__name__)


@login_required
@require_GET
def check_memo_state(request, pk):
    print("check")
    memo = get_object_or_404(Memo, pk=pk, user=request.user)

    if memo.state in ("done", "cancel"):
        return JsonResponse(
            {
                "can_validate": False,
                "message": _("Cette tâche est déjà terminée ou annulée."),
            },
            status=400,
        )

    return JsonResponse({"can_validate": True})


@login_required
@require_POST
def memo_mark_done(request, pk):
    memo = get_object_or_404(Memo, pk=pk, user=request.user)

    success = memo.check_if_state_is_cancel_or_done()

    if not success:
        return JsonResponse(
            {
                "success": False,
                "message": _("Cette tâche est déjà terminée ou annulée."),
            },
            status=400,
        )

    new_date_str = request.POST.get("new_date")

    if not new_date_str:
        return JsonResponse(
            {"success": False, "message": _("Date manquante.")}, status=400
        )
    new_date = parse_date(new_date_str)
    if not new_date:
        return JsonResponse(
            {"success": False, "message": _("Date invalide.")}, status=400
        )

    success, message = memo.validate_element(new_date)

    if success:
        return JsonResponse(
            {"success": True, "done_date": memo.done_date.strftime("%Y-%m-%d")}
        )
    else:
        return JsonResponse({"success": False, "message": message})


def log_memo_history(memo, user, action, changes=None):
    return MemoHistory.objects.create(
        memo=memo,
        action=action,
        changed_by=user,
        changes=changes or {},
    )
