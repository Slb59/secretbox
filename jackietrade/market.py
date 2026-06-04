from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from config import env

from .forms import MarketDataSyncForm
from .import_data import YFinanceImporter


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

        form = MarketDataSyncForm(request.POST)

        if form.is_valid():

            assets = form.cleaned_data["assets"]
            period = form.cleaned_data["period"]
            interval = form.cleaned_data["interval"]

            importer = YFinanceImporter()

            total_created = 0

            for asset in assets:

                created_count = importer.import_history(
                    asset=asset,
                    period=period,
                    interval=interval,
                )

                total_created += created_count
                asset.last_sync_at = timestamps

            messages.success(
                request,
                f"{total_created} candles importées."
            )

        return render(
            request,
            self.template_name,
            {
                "form": form,
            }
        )