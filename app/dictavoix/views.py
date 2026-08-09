import re

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Prefetch
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, TemplateView

from .forms import DictavoixSessionForm
from .models import DictavoixExercise, DictavoixTheme


class DictavoixDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dictavoix/dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        if not (
            request.user.is_superuser
            or request.user.groups.filter(name="dictavoix_access").exists()
        ):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        themes = (
            DictavoixTheme.objects.prefetch_related(
                Prefetch("dictionary_words"),
                Prefetch("exercises"),
            )
            .annotate(
                word_count=Count("dictionary_words"), exercise_count=Count("exercises")
            )
            .order_by("name")
        )
        context.update(
            {
                "themes": themes,
                "title": "Dictavoix",
                "description": "Dictation exercises grouped by theme.",
            }
        )
        return context


class ExerciseDetailView(LoginRequiredMixin, DetailView):
    model = DictavoixExercise
    template_name = "dictavoix/exercise_detail.html"
    context_object_name = "exercise"

    def dispatch(self, request, *args, **kwargs):
        if not (
            request.user.is_superuser
            or request.user.groups.filter(name="dictavoix_access").exists()
        ):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        text = self.object.text.strip()
        context["audio_script"] = self.build_audio_script(text)
        context["dictionary_words"] = self.object.theme.dictionary_words.order_by(
            "word"
        )
        context["form"] = DictavoixSessionForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = DictavoixSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.exercise = self.object
            session.save()
            messages.success(request, "Session Dictavoix enregistrée.")
            return redirect(reverse("dictavoix:exercise_detail", args=[self.object.pk]))

        context = self.get_context_data(object=self.object)
        context["form"] = form
        return self.render_to_response(context)

    def build_audio_script(self, text):
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\\s+", text) if s.strip()]
        script = []

        # Normal speed first read
        script.append({"label": "normal", "text": text, "repeat": 1})

        # Repeat each sentence 4 times slowly
        for sentence in sentences:
            safe_sentence = sentence
            script.append(
                {"label": "slow_sentence", "text": safe_sentence, "repeat": 4}
            )

        # Slow full text read, then normal speed again
        script.append({"label": "slow", "text": text, "repeat": 1})
        script.append({"label": "normal", "text": text, "repeat": 1})

        return script
