from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from config import env

from .watchlistmodels import Watchlist


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "jackietrade/dashboard.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        user = self.request.user

        # service = DashboardService()

        # context.update(
        #     service.get_context()
        # )

        watchlists = Watchlist.objects.filter(user=user)
        current_watchlist = watchlists.filter(is_default=True).first()

        context.update(
            {
                "title": _("Suivi de portefeuille"),
                "logo_url": env("JACKIETRADE_LOGO_URL"),
                "watchlists": watchlists,
                "current_watchlist": current_watchlist,
                "assets": current_watchlist.assets.all() if current_watchlist else [],
            }
        )

        return context
