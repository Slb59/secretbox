"""Views for the samicheck application.
Dashboard
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .models import SamiCategory, SamiDay, SamiEntry, SamiIndicator


class SamicheckDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "samicheck-dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        indicators = list(
            SamiIndicator.objects.select_related("category").order_by(
                "category__name", "title"
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
                "date": SamiDay.objects.order_by("-date").first(),
                "categories": SamiCategory.objects.all(),
                "indicators": indicators,
                "entries": SamiEntry.objects.all(),
                "table_columns": table_columns,
                "table_data": table_data,
            }
        )
        return context
