"""Views for todo model on the dashboard application
Dashboard, edit, create, delete, and list views.
"""

import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Min, Q
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from .filters import MemoFilterForm
from .memo import Memo

logger = logging.getLogger(__name__)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def apply_filters(self, todos, data):
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
                    todos = todos.filter(**target(value))
                else:
                    todos = todos.filter(**{target: value})

        range_filters = {
            "planned_date_start": ("planned_date__gte", "planned_date_start"),
            "planned_date_end": ("planned_date__lte", "planned_date_end"),
            "duration_min": ("duration__gte", "duration_min"),
            "duration_max": ("duration__lte", "duration_max"),
            "done_date_start": ("done_date__gte", "done_date_start"),
            "done_date_end": ("done_date__lte", "done_date_end"),
        }

        for field, (lookup, data_key) in range_filters.items():
            value = data.get(data_key)
            if value is not None:
                todos = todos.filter(**{lookup: value})
                if "done_date" in lookup:
                    todos = todos.exclude(done_date__isnull=True)

        return todos

    def get_queryset_by_rights(self, user):
        """Filtering by rights"""
        logger.info(
            _("Recherche dans Dashboard get_queryset_by_rights par l'utilisateur %s"),
            user,
        )

        if user.is_superuser:
            qs = Todo.objects.all()
        else:
            qs = Todo.objects.filter(Q(user=user) | Q(who=user))

        qs = qs.distinct().prefetch_related("who")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = TodoFilterForm(self.request.GET or None)
        user = self.request.user
        todos = self.get_queryset_by_rights(user)

        if form.is_valid():
            todos = self.apply_filters(todos, form.cleaned_data)
        todos = todos.annotate(first_who=Min("who__trigram")).order_by(
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
                "logo_url": "/static/images/secretbox/logo_sb2.png",
                "todos": todos,
                "form": form,
                "request": self.request,
            }
        )

        return context

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        context = {}

        if pk:
            # Empêcher plusieurs timers
            if not request.user.stopwatch:
                request.user.stopwatch = True
                request.user.save()

                todo = get_object_or_404(Todo, pk=pk, who=request.user)
                request.session["active_timer_id"] = pk
                request.session["active_timer_start"] = timezone.now().isoformat()
                context["active_todo"] = todo
                context["timer_started"] = True
            else:
                # Un timer est déjà en cours → on reste sur la page
                context["timer_started"] = True
                active_id = request.session.get("active_timer_id")
                if active_id:
                    context["active_todo"] = Todo.objects.filter(pk=active_id).first()
        else:
            context["timer_started"] = False

        context["todos"] = Todo.objects.filter(who=request.user)
        return self.render_to_response(context)
