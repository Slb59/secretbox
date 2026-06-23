from itertools import groupby

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, UpdateView

from config import env

from .assetforms import AssetForm
from .assetmodels import Asset, Sector


class AssetListView(LoginRequiredMixin, ListView):
    model = Asset
    template_name = "jackietrade/asset_list.html"
    context_object_name = "assets"

    def get_queryset(self):
        return (
            Asset.objects.filter(is_active=True)
            .select_related("sector")
            .prefetch_related("watchlists")
            .order_by("sector__name", "name")
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        assets = context["assets"]

        grouped_assets = []

        for sector, asset_group in groupby(assets, key=lambda x: x.sector):
            grouped_assets.append(
                {
                    "sector": sector,
                    "assets": list(asset_group),
                }
            )

        context["title"] = _("Les actifs")
        context["logo_url"] = env("JACKIETRADE_LOGO_URL")
        context["sectors"] = Sector.objects.prefetch_related("assets").order_by("name")
        context["grouped_assets"] = grouped_assets
        return context


class AssetUpdateView(LoginRequiredMixin, UpdateView):
    model = Asset
    form_class = AssetForm
    template_name = "jackietrade/asset_form.html"
    success_url = reverse_lazy("jackietrade:asset_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["title"] = _("Les actifs")
        context["logo_url"] = env("JACKIETRADE_LOGO_URL")

        return context
