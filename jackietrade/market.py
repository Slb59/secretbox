from django.contrib import messages
from django.shortcuts import render
from django.views import View

from .forms import MarketDataSyncForm
from market_data.services.importers.yfinance_importer import (
    YFinanceImporter,
)


class MarketDataSyncView(View):

    template_name = "jackietrade/sync_market_data.html"

    def get(self, request):

        form = MarketDataSyncForm()

        return render(
            request,
            self.template_name,
            {
                "form": form,
            }
        )

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