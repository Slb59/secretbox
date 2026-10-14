"""Views for the samicheck application.
Dashboard
"""

import json
from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from config import env

from .models import SamiCategory, SamiDay, SamiEntry, SamiIndicator


class SamicheckDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "samicheck-dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        indicators = list(
            SamiIndicator.objects.select_related("category").order_by(
                "category__display_order",
                "category__name",
                "display_order",
                "title",
            )
        )
        days = SamiDay.objects.prefetch_related("entries").order_by("-date")

        table_columns = [
            {
                "title": f"{indicator.category.name} - {indicator.title}",
                "field": f"indicator_{indicator.pk}",
            }
            for indicator in indicators
        ]
        table_data = []
        for day in days:
            entry_values = {
                entry.indicator_id: entry.value for entry in day.entries.all()
            }
            row = {"date": day.date.isoformat()}
            row.update(
                {
                    f"indicator_{indicator.pk}": entry_values.get(indicator.pk)
                    for indicator in indicators
                }
            )
            table_data.append(row)

        context.update(
            {
                "title": _("Tableau de bord SAMI"),
                "logo_url": env("SAMI_LOGO_URL"),
                "date": SamiDay.objects.order_by("-date").first(),
                "categories": SamiCategory.objects.all(),
                "indicators": indicators,
                "entries": SamiEntry.objects.all(),
                "table_columns": table_columns,
                "table_data": table_data,
                "today": timezone.localdate().isoformat(),
            }
        )
        return context


@login_required
@require_POST
def create_day(request):
    try:
        payload = json.loads(request.body)
        if not isinstance(payload, dict):
            raise ValueError
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
        return JsonResponse(
            {"success": False, "errors": {"form": "Données invalides."}},
            status=400,
        )

    try:
        day_date = date.fromisoformat(payload.get("date", ""))
    except (TypeError, ValueError):
        return JsonResponse(
            {"success": False, "errors": {"date": "Date invalide."}},
            status=400,
        )

    indicators = list(SamiIndicator.objects.all())
    entries = []
    errors = {}
    row = {"date": day_date.isoformat()}

    for indicator in indicators:
        field_name = f"indicator_{indicator.pk}"
        raw_value = payload.get(field_name, "")
        if raw_value in (None, ""):
            row[field_name] = None
            continue
        try:
            value = int(raw_value)
        except (TypeError, ValueError):
            errors[field_name] = "Saisissez un nombre entier."
            continue
        if value < 0 or value > indicator.max_level:
            errors[field_name] = (
                f"La valeur doit être comprise entre 0 et {indicator.max_level}."
            )
            continue
        entries.append(SamiEntry(indicator=indicator, value=value))
        row[field_name] = value

    if errors:
        return JsonResponse({"success": False, "errors": errors}, status=400)

    try:
        with transaction.atomic():
            day = SamiDay.objects.create(date=day_date)
            for entry in entries:
                entry.day = day
            SamiEntry.objects.bulk_create(entries)
    except IntegrityError:
        return JsonResponse(
            {"success": False, "errors": {"date": "Cette journée existe déjà."}},
            status=400,
        )

    return JsonResponse({"success": True, "row": row})
