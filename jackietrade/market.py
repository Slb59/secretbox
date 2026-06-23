import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from config import env

from .import_data import YFinanceImporter
from .marketforms import MarketDataSyncForm

logger = logging.getLogger(__name__)


class MarketDataSyncView(LoginRequiredMixin, TemplateView):
    template_name = "jackietrade/import_data.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = MarketDataSyncForm(
            self.request.POST or None,
            user=self.request.user,
        )

        user = self.request.user

        context.update(
            {
                "title": _("Synchronisation des données marché"),
                "logo_url": env("JACKIETRADE_LOGO_URL"),
                "form": form,
                "request": self.request,
            }
        )

        return context

    def post(self, request):

        form = MarketDataSyncForm(request.POST, user=self.request.user)

        if form.is_valid():
            assets = form.cleaned_data["assets"]
            period = form.cleaned_data["period"]
            interval = form.cleaned_data["interval"]

            logger.info(
                "Synchronisation demandée par %s",
                self.request.user.username,
            )

            importer = YFinanceImporter()

            total_created = 0

            logger.info(
                "%s actifs sélectionnés",
                len(assets),
            )

            for asset in assets:
                logger.info(
                    "Traitement de %s",
                    asset.symbol,
                )

                created_count = importer.import_history(
                    asset=asset,
                    period=period,
                    interval=interval,
                )

                logger.info(
                    "%s : %s candles créées",
                    asset.symbol,
                    created_count,
                )

                total_created += created_count
                asset.last_sync_at = timezone.now()
                asset.save(update_fields=["last_sync_at"])

            messages.success(request, f"{total_created} candles importées.")

        return render(
            request,
            self.template_name,
            {
                "form": form,
            },
        )
