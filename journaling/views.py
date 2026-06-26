import logging
from datetime import date, timezone

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Min, Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, View

from config import env

from .filters import MemoFilterForm
from .forms import MemoForm, MemoReportForm, MemoValidateForm
from .memo import Memo, MemoHistory
from .utils import log_memo_history

logger = logging.getLogger(__name__)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "journaling/dashboard.html"

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

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        context = self.get_context_data(**kwargs)

        if pk:
            # Empêcher plusieurs timers
            if not request.user.stopwatch:
                request.user.stopwatch = True
                request.user.save()

                memo = get_object_or_404(Memo, pk=pk, who=request.user)
                request.session["active_timer_id"] = pk
                request.session["active_timer_start"] = timezone.now().isoformat()
                context["active_memo"] = memo
                context["timer_started"] = True
            else:
                # Un timer est déjà en cours → on reste sur la page
                context["timer_started"] = True
                active_id = request.session.get("active_timer_id")
                if active_id:
                    context["active_memo"] = Memo.objects.filter(pk=active_id).first()
        else:
            context["timer_started"] = False

        context["memos"] = Memo.objects.filter(who=request.user)
        return self.render_to_response(context)

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


class MemoCreateView(LoginRequiredMixin, CreateView):
    model = Memo
    form_class = MemoForm
    template_name = "journaling/add_template.html"
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
    template_name = "journaling/add_template.html"
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
    template_name = "journaling/history.html"
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
