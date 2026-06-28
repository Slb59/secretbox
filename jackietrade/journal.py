from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from config import env

from .journalforms import JournalForm
from .journalmodels import TradeJournalEntry


class JournalListView(LoginRequiredMixin, ListView):
    model = TradeJournalEntry
    template_name = "journal_list.html"
    context_object_name = "journals"

    def get_queryset(self):
        return TradeJournalEntry.objects.filter(user=self.request.user).order_by(
            "session_date"
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        # journals = context["journals"]

        context["title"] = _("Les journaux de trade")
        context["logo_url"] = env("JACKIETRADE_LOGO_URL")

        return context


class JournalUpdateView(LoginRequiredMixin, UpdateView):
    model = TradeJournalEntry
    form_class = JournalForm

    template_name = "journal_form.html"
    success_url = reverse_lazy("jackietrade:journal_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["journals"] = TradeJournalEntry.objects.filter(
            user=self.request.user
        ).order_by("session_date")

        return context


class JournalDeleteView(LoginRequiredMixin, DeleteView):
    def post(self, request, pk):

        journal = get_object_or_404(
            TradeJournalEntry,
            pk=pk,
            user=request.user,
        )

        journal.delete()

        messages.success(request, "Suppression effectuée.")

        return redirect("jackietrade:journal_list")


class JournalCreateView(LoginRequiredMixin, CreateView):
    model: type[TradeJournalEntry] = TradeJournalEntry
    form_class: type[JournalForm] = JournalForm

    template_name = "journal_form.html"
    success_url = reverse_lazy("jackietrade:journal_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
