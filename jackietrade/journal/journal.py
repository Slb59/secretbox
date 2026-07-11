from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView, ListView, View

from config import env

from .decisionform import DecisionForm
from .journalheader import JournalHeaderForm
from .journalmodels import Analysis, TradeJournalEntry, TradeJournalScreenshot
from .observation import ObservationForm
from .resultform import ResultForm


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


class JournalView(LoginRequiredMixin, View):
    model = TradeJournalEntry

    template_name = "journal_form.html"
    success_url = reverse_lazy("jackietrade:journal_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        obj = self.object

        context["header_form"] = JournalHeaderForm(instance=obj, prefix="header")

        context["observation_form"] = ObservationForm(
            instance=obj, prefix="observation"
        )

        context["decision_form"] = DecisionForm(instance=obj, prefix="decision")

        context["result_form"] = ResultForm(instance=obj, prefix="result")

        context["analysis"] = Analysis.compute(obj)

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


class ObservationUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):

        journal = get_object_or_404(
            TradeJournalEntry,
            pk=pk,
            user=request.user,
        )

        form = ObservationForm(request.POST, instance=journal, prefix="observation")

        if form.is_valid():
            form.save()
            messages.success(request, "Observation mise à jour.")
        else:
            messages.error(request, "Erreur lors de la mise à jour de l'observation.")

        return redirect("jackietrade:journal_list")


class DecisionUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):

        journal = get_object_or_404(
            TradeJournalEntry,
            pk=pk,
            user=request.user,
        )

        form = DecisionForm(request.POST, instance=journal, prefix="decision")

        if form.is_valid():
            form.save()
            messages.success(request, "Décision mise à jour.")
        else:
            messages.error(request, "Erreur lors de la mise à jour de la décision.")

        return redirect("jackietrade:journal_list")


class ResultUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):

        journal = get_object_or_404(
            TradeJournalEntry,
            pk=pk,
            user=request.user,
        )

        form = ResultForm(request.POST, instance=journal, prefix="result")

        if form.is_valid():
            form.save()
            messages.success(request, "Résultat mis à jour.")
        else:
            messages.error(request, "Erreur lors de la mise à jour du résultat.")

        return redirect("jackietrade:journal_list")


class AnalysisView(LoginRequiredMixin, View):
    def get(self, request, pk):

        journal = get_object_or_404(
            TradeJournalEntry,
            pk=pk,
            user=request.user,
        )

        analysis = Analysis.compute(journal)

        context = {
            "journal": journal,
            "analysis": analysis,
        }

        return render(request, "journal_analysis.html", context)


class ScreenshotCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):

        # journal = get_object_or_404(
        #     TradeJournalEntry,
        #     pk=pk,
        #     user=request.user,
        # )

        # Logic to create a screenshot for the journal entry
        # This is a placeholder for the actual implementation
        messages.success(request, "Capture d'écran créée avec succès.")

        return redirect("jackietrade:journal_list")


class ScreenshotDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk, screenshot_id):

        journal = get_object_or_404(
            TradeJournalEntry,
            pk=pk,
            user=request.user,
        )

        screenshot = get_object_or_404(
            TradeJournalScreenshot,
            pk=screenshot_id,
            journal=journal,
        )

        screenshot.delete()
        messages.success(request, "Capture d'écran supprimée avec succès.")

        return redirect("jackietrade:journal_list")
