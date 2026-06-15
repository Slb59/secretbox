from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django import forms

from .models import Watchlist, Asset
from .watchlistforms import WatchlistForm, WatchlistAddAssetForm
from config import env

class WatchlistListView(LoginRequiredMixin, ListView):
    model = Watchlist
    template_name = "jackietrade/watchlist_list.html"

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Mes watchlistes")
        context["logo_url"] = env("JACKIETRADE_LOGO_URL")
        return context


class WatchlistCreateView(LoginRequiredMixin, CreateView):
    model = Watchlist
    form_class = WatchlistForm

    template_name = "jackietrade/watchlist_form.html"
    success_url = reverse_lazy("jackietrade:dashboard")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)




class WatchlistUpdateView(LoginRequiredMixin, UpdateView):
    model = Watchlist
    form_class = WatchlistForm

    template_name = "jackietrade/watchlist_form.html"
    success_url = reverse_lazy("jackietrade:watchlist_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        print("VIEW USED:", self.__class__)
        print("SUCCESS URL:", self.success_url)
        return self.success_url

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["assets"] = Asset.objects.filter(
            watchlistitem__watchlist=self.object
        ).order_by("symbol")

        return context


class WatchlistDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):

        watchlist = get_object_or_404(
            Watchlist,
            pk=pk,
            user=request.user,
        )

        if watchlist.assets.count() > 0 :

            messages.error(
                request,
                "Cette liste contient des actifs."
            )

        else:

            watchlist.delete()

            messages.success(
                request,
                "Suppression effectuée."
            )

        return redirect(
            "jackietrade:watchlist_list"
        )


class ToggleAssetWatchlistView(LoginRequiredMixin, View):

    def post(self, request, pk):
        watchlist = get_object_or_404(
            Watchlist,
            pk=pk,
            user=request.user
        )

        asset_id = request.POST.get("asset_id")
        asset = get_object_or_404(Asset, pk=asset_id)

        if asset in watchlist.assets.all():
            watchlist.assets.remove(asset)
        else:
            watchlist.assets.add(asset)

        return redirect(request.META.get("HTTP_REFERER", "/"))


class WatchlistAddAssetView(LoginRequiredMixin,TemplateView):

    template_name = "jackietrade/watchlist_add_asset.html"

    def dispatch(self, request, *args, **kwargs):

        self.watchlist = get_object_or_404(
            Watchlist,
            pk=kwargs["pk"],
            user=request.user,
        )

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["watchlist"] = self.watchlist
        context["form"] = WatchlistAddAssetForm(watchlist=self.watchlist)

        return context

    def post(self, request, *args, **kwargs):

        form = WatchlistAddAssetForm(request.POST, watchlist=self.watchlist)

        if form.is_valid():

            assets = form.cleaned_data["assets"]

            for asset in assets:
                self.watchlist.add_asset(asset)

            messages.success(
                request,
                f"{len(assets)} actif(s) ajouté(s)."
            )

            return redirect(
                "jackietrade:watchlist_update",
                pk=self.watchlist.pk,
            )

        return self.render_to_response(
            {
                "watchlist": self.watchlist,
                "form": form,
            }
        )