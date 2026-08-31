import json
import logging
from datetime import date

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Min, Q
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, View

from config import env

from .choices import (
    CATEGORY_CHOICES,
    PERIODIC_CHOICES,
    PLACE_CHOICES,
    PRIORITY_CHOICES,
)
from .filters import MemoFilterForm
from .forms import MemoForm, MemoReportForm, MemoValidateForm
from .memo import Memo, MemoHistory
from .utils import log_memo_history

logger = logging.getLogger(__name__)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = MemoFilterForm(self.request.GET or None)
        user = self.request.user
        memos = self.get_queryset_by_rights(user)

        if form.is_valid():
            memos = self.apply_filters(memos, form.cleaned_data)
        memos = memos.annotate(first_who=Min("who__trigram")).order_by(
            "planned_date",
            "priority",
            "periodic",
            "first_who",
            "place",
            "duration",
            "pk",
        )
        context.update(
            {
                "title": _("Bienvenue dans SecretBox"),
                "logo_url": env("SECRETBOX_LOGO_URL"),
                "memos": memos,
                "form": form,
                "request": self.request,
            }
        )

        return context

    def apply_filters(self, memos, data):
        """Apply filters to the queryset"""

        simple_filters = {
            "state": "state",
            "category": "category",
            "priority": "priority",
            "description": lambda v: {"description__icontains": v},
            "appointment": "appointment",
            "who": "who",
            "place": "place",
            "periodic": "periodic",
            "done_date_isnull": lambda v: {"done_date__isnull": v},
        }

        for field, target in simple_filters.items():
            value = data.get(field)
            if value:
                if callable(target):
                    memos = memos.filter(**target(value))
                else:
                    memos = memos.filter(**{target: value})

        range_filters = {
            "planned_date_start": ("planned_date__gte", "planned_date_start"),
            "planned_date_end": ("planned_date__lte", "planned_date_end"),
            "duration_min": ("duration__gte", "duration_min"),
            "duration_max": ("duration__lte", "duration_max"),
            "done_date_start": ("done_date__gte", "done_date_start"),
            "done_date_end": ("done_date__lte", "done_date_end"),
        }

        for _field, (lookup, data_key) in range_filters.items():
            value = data.get(data_key)
            if value is not None:
                memos = memos.filter(**{lookup: value})
                if "done_date" in lookup:
                    memos = memos.exclude(done_date__isnull=True)

        return memos

    def get_queryset_by_rights(self, user):
        """Filtering by rights"""

        if user.is_superuser:
            qs = Memo.objects.all()
        else:
            qs = Memo.objects.filter(Q(user=user) | Q(who=user))

        qs = qs.distinct().prefetch_related("who")
        return qs


class DashboardDataView(DashboardView):
    """Return memos as JSON for Tabulator consumption.

    Reuses DashboardView filtering logic so URL query params keep parity
    with the HTML form filters.
    """

    def get(self, request, *args, **kwargs):
        form = MemoFilterForm(request.GET or None)
        memos = self.get_queryset_by_rights(request.user)

        if form.is_valid():
            memos = self.apply_filters(memos, form.cleaned_data)

        memos = memos.annotate(first_who=Min("who__trigram")).order_by(
            "planned_date",
            "priority",
            "periodic",
            "first_who",
            "place",
            "duration",
            "pk",
        )

        data = []
        for m in memos.prefetch_related("who"):
            data.append(
                {
                    "pk": m.pk,
                    "state": m.get_state_display(),
                    "duration": m.duration,
                    "description": m.description,
                    "appointment": m.get_appointment_display()
                    if hasattr(m, "get_appointment_display")
                    else (m.appointment or ""),
                    "category": m.get_category_display(),
                    "who": ", ".join([u.trigram for u in m.who.all()]),
                    "place": m.get_place_display(),
                    "periodic": m.get_periodic_display(),
                    "planned_date": m.planned_date.isoformat()
                    if m.planned_date
                    else "",
                    "priority": m.get_priority_display(),
                    "done_date": m.done_date.isoformat() if m.done_date else "",
                    "note": m.note or "",
                }
            )

        return JsonResponse(data, safe=False)


class MemoStartDayView(LoginRequiredMixin, View):
    """Set the selected date for every todo item at the earliest todo date."""

    def post(self, request, *args, **kwargs):
        try:
            raw_date = request.POST.get("planned_date")
            if not raw_date:
                try:
                    payload = json.loads(request.body or "{}")
                    raw_date = payload.get("planned_date")
                except json.JSONDecodeError:
                    raw_date = None

            target_date = date.fromisoformat(raw_date) if raw_date else date.today()
        except ValueError:
            return JsonResponse(
                {"success": False, "error": "Date invalide."},
                status=400,
            )

        queryset = Memo.objects.filter(state="todo")
        if not request.user.is_superuser:
            queryset = queryset.filter(
                Q(user=request.user) | Q(who=request.user)
            ).distinct()

        earliest_date = queryset.aggregate(earliest=Min("planned_date"))["earliest"]
        if earliest_date is None:
            return JsonResponse(
                {"success": True, "updated": 0, "target_date": target_date.isoformat()}
            )

        updated_count = queryset.filter(planned_date=earliest_date).update(
            planned_date=target_date
        )
        return JsonResponse(
            {
                "success": True,
                "updated": updated_count,
                "target_date": target_date.isoformat(),
            }
        )


class MemoUpdateAPIView(LoginRequiredMixin, View):
    """API endpoint for updating memo fields via PATCH request."""

    def patch(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            pk = data.get("pk")
            memo = get_object_or_404(Memo, pk=pk)

            logger.info(f"Updating memo {pk} with data: {data}")

            # Check permissions
            if not (memo.can_edit(request.user) or memo.can_edit_limited(request.user)):
                return JsonResponse(
                    {"success": False, "error": "Permission denied"},
                    status=403,
                )

            def build_choice_map(choices):
                mapping = {}
                for key, label in choices:
                    mapping[key] = key
                    mapping[str(label)] = key
                return mapping

            # Accept both raw stored values and display labels from the table.
            state_map = build_choice_map(Memo.STATE_CHOICES)
            priority_map = build_choice_map(PRIORITY_CHOICES)
            category_map = build_choice_map(CATEGORY_CHOICES)
            periodic_map = build_choice_map(PERIODIC_CHOICES)
            place_map = build_choice_map(PLACE_CHOICES)
            appointment_map = build_choice_map(Memo.APPOINTEMENT_CHOICES)

            # Update fields if provided
            if "duration" in data and data["duration"] is not None:
                try:
                    memo.duration = int(data["duration"])
                except (ValueError, TypeError):
                    pass
            if "description" in data:
                memo.description = data["description"]
            if "note" in data:
                memo.note = data["note"]
            if "place" in data and data["place"]:
                memo.place = place_map.get(str(data["place"]), memo.place)
            if "state" in data and data["state"]:
                memo.state = state_map.get(str(data["state"]), memo.state)
            if "priority" in data and data["priority"]:
                memo.priority = priority_map.get(str(data["priority"]), memo.priority)
            if "category" in data and data["category"]:
                memo.category = category_map.get(str(data["category"]), memo.category)
            if "periodic" in data and data["periodic"]:
                memo.periodic = periodic_map.get(str(data["periodic"]), memo.periodic)
            if "appointment" in data and data["appointment"]:
                memo.appointment = appointment_map.get(
                    str(data["appointment"]), memo.appointment
                )
            if "planned_date" in data and data["planned_date"]:
                memo.planned_date = data["planned_date"]
            if "done_date" in data and data["done_date"]:
                memo.done_date = data["done_date"]
            if "who" in data and data["who"] not in (None, ""):
                user_model = get_user_model()
                values = [
                    value.strip()
                    for value in str(data["who"]).split(",")
                    if value.strip()
                ]
                assignees = list(user_model.objects.filter(trigram__in=values))
                memo.who.set(assignees)

            memo.save()

            return JsonResponse(
                {"success": True, "message": "Memo updated successfully"}
            )

        except Memo.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Memo not found"},
                status=404,
            )
        except Exception as e:
            logger.error(f"Error updating memo: {str(e)}")
            return JsonResponse(
                {"success": False, "error": str(e)},
                status=400,
            )


class MemoCreateView(LoginRequiredMixin, CreateView):
    model = Memo
    form_class = MemoForm
    template_name = "add_template.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Nouvelle entrée")
        context["logo_url"] = env("SECRETBOX_LOGO_URL")
        return context

    def form_valid(self, form):
        memo = form.save(commit=False)
        memo.user = self.request.user
        memo.save()

        # Afficher les assignés
        memo.who.add(self.request.user)
        assignees = memo.who.all()
        print(f"Assignés: {[user.trigram for user in assignees]}")
        memo.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning(f"Form invalid:{self.__class__.__name__} {form.errors}")
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MemoUpdateView(LoginRequiredMixin, UpdateView):
    model = Memo
    form_class = MemoForm
    template_name = "add_template.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Modifier l'entrée")
        context["logo_url"] = env("SECRETBOX_LOGO_URL")
        return context

    def dispatch(self, request, *args, **kwargs):
        memo = self.get_object()
        if not memo.can_view(request.user):
            return HttpResponseForbidden(_("Vous ne pouvez pas voir cet élément."))

        if not (memo.can_edit(request.user) or memo.can_edit_limited(request.user)):
            return HttpResponseForbidden(_("Vous ne pouvez pas modifier cet élément."))

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # pour le formulaire
        return kwargs


class MemoDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        memo = get_object_or_404(Memo, pk=pk)
        if memo.state != "cancel":
            memo.state = "cancel"
            memo.note = f"*** supprimé {date.today()} ***\n{memo.note}"
            memo.save()
        return redirect("home")

    def dispatch(self, request, *args, **kwargs):
        memo = self.get_object()
        if not memo.can_delete(request.user):
            return HttpResponseForbidden(_("Vous ne pouvez pas supprimer cet élément."))
        return super().dispatch(request, *args, **kwargs)


class MemoUnDeleteView(LoginRequiredMixin, View):
    model = Memo
    success_url = reverse_lazy("home")

    def post(self, request, pk, *args, **kwargs):
        memo = get_object_or_404(Memo, pk=pk)
        if not memo.can_undelete(request.user):
            messages.error(request, _("Vous ne pouvez pas restaurer cet élément."))
            return redirect("home")

        try:
            memo.undelete_element()
            messages.success(request, _("Memo restauré"))
        except Exception as e:
            messages.error(request, _("Erreur lors de la restauration : ") + str(e))

        return redirect("home")


class MemoValidateView(LoginRequiredMixin, UpdateView):
    model = Memo
    form_class = MemoValidateForm
    template_name = "generic/add_template.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        memo = form.save(commit=False)
        date_to_validate = form.cleaned_data["planned_date"]
        if date_to_validate <= memo.original_planned_date:
            messages.error(
                self.request,
                _(
                    f"La date {date_to_validate} doit être postérieure"
                    + f" la date planifiée actuelle {memo.original_planned_date}."
                ),
            )
            return redirect(self.success_url)
        with transaction.atomic():
            memo.state = "todo"
            memo.report_date = None
            memo.done_date = date.today()
            log_memo_history(
                memo=memo,
                user=memo.user,
                action="updated",
                changes={"field": "description", "old": "foo", "new": "bar"},
            )
            memo.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        memo = self.get_object()
        if memo.state == "done" or memo.state == "cancel":
            messages.error(request, _("Impossible de valider une tâche déjà terminée."))
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        memo = self.get_object()
        context.update(
            {
                "title": _("Validation de l'opération"),
                "logo_url": env("SECRETBOX_LOGO_URL"),
                "description": memo.description,
            }
        )
        return context


class MemoReportView(LoginRequiredMixin, UpdateView):
    model = Memo
    form_class = MemoReportForm
    template_name = "generic/add_template.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        memo = form.save(commit=False)
        memo.state = "report"
        if memo.report_date is None:
            memo.report_date = date.today()
        memo.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        memo = self.get_object()
        if memo.state == "done" or memo.state == "cancel":
            messages.error(
                request, _("Impossible de reporter une tâche déjà terminée.")
            )
            return redirect(self.success_url)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todo = self.get_object()
        context.update(
            {
                "title": _("Report de l'opération"),
                "logo_url": env("SECRETBOX_LOGO_URL"),
                "description": todo.description,
            }
        )
        return context


class MemoHistoryView(LoginRequiredMixin, ListView):
    model = MemoHistory
    template_name = "history.html"
    context_object_name = "history"

    def get_queryset(self):
        self.memo = get_object_or_404(Memo, pk=self.kwargs["pk"])
        history_context = MemoHistory.objects.filter(memo=self.memo).order_by(
            "-timestamp"
        )
        return history_context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["memo"] = self.memo
        context["title"] = _("Historique de modifications")
        context["logo_url"] = (env("SECRETBOX_LOGO_URL"),)
        return context
