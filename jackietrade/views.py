from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from config import env

class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "jackietrade/dashboard.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # service = DashboardService()

        # context.update(
        #     service.get_context()
        # )
        context.update(
            {
                "title": _("Bienvenue dans JackieTrade"),
                "logo_url": env("JACKIETRADE_LOGO_URL"),
            }
        )

        return context