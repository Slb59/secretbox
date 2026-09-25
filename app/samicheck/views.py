"""Views for the samicheck application.
Dashboard
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .models import SamiCategory, SamiDay, SamiEntry, SamiIndicator


class SamicheckDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "date": SamiDay.objects.order_by("-date").first(),
                "categories": SamiCategory.objects.all(),
                "indicators": SamiIndicator.objects.all(),
                "entries": SamiEntry.objects.all(),
            }
        )
        return context
