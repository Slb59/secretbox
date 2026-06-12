from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from .models import Watchlist, Asset
from .watchlistforms import WatchlistForm

class WatchlistListView(LoginRequiredMixin, ListView):
    model = Watchlist
    template_name = "jackietrade/watchlist_list.html"

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)


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


class WatchlistDeleteView(LoginRequiredMixin, DeleteView):
    model = Watchlist
    template_name = "jackietrade/confirm_delete.html"
    success_url = reverse_lazy("jackietrade:watchlist_list")

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)



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