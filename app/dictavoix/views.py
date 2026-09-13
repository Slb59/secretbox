import json
import re

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.db.models import Count, Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, TemplateView

from .forms import DictavoixDictionaryWordForm, DictavoixSessionForm
from .models import DictavoixExercise, DictavoixTheme


class DictavoixAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        if not (
            request.user.is_superuser
            or request.user.groups.filter(name="dictavoix_access").exists()
        ):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class DictavoixDashboardView(LoginRequiredMixin, DictavoixAccessMixin, TemplateView):
    template_name = "dictavoix/dashboard.html"

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


class DictavoixDictionaryView(LoginRequiredMixin, DictavoixAccessMixin, TemplateView):
    template_name = "dictavoix/dictionary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["theme"] = get_object_or_404(DictavoixTheme, pk=self.kwargs["theme_pk"])
        context["title"] = f"Dictionnaire - {context['theme'].name}"
        return context


class DictavoixDictionaryWordsAPIView(LoginRequiredMixin, DictavoixAccessMixin, View):
    def get_theme(self, theme_pk):
        return get_object_or_404(DictavoixTheme, pk=theme_pk)

    def get(self, request, theme_pk):
        theme = self.get_theme(theme_pk)
        return JsonResponse(
            [self.serialize(word) for word in theme.dictionary_words.order_by("word")],
            safe=False,
        )

    def post(self, request, theme_pk):
        theme = self.get_theme(theme_pk)
        data = self.parse_json(request)
        if isinstance(data, JsonResponse):
            return data
        form = DictavoixDictionaryWordForm(data)
        if not form.is_valid():
            return JsonResponse({"errors": form.errors}, status=400)
        word = form.save(commit=False)
        word.theme = theme
        try:
            word.save()
        except IntegrityError:
            return JsonResponse(
                {"error": "Ce mot existe déjà dans ce thème."}, status=400
            )
        return JsonResponse(self.serialize(word), status=201)

    def patch(self, request, theme_pk):
        theme = self.get_theme(theme_pk)
        data = self.parse_json(request)
        if isinstance(data, JsonResponse):
            return data
        word = get_object_or_404(theme.dictionary_words, pk=data.get("pk"))
        form = DictavoixDictionaryWordForm(data, instance=word)
        if not form.is_valid():
            return JsonResponse({"errors": form.errors}, status=400)
        return JsonResponse(self.serialize(form.save()))

    def delete(self, request, theme_pk):
        theme = self.get_theme(theme_pk)
        data = self.parse_json(request)
        if isinstance(data, JsonResponse):
            return data
        word = get_object_or_404(theme.dictionary_words, pk=data.get("pk"))
        word.delete()
        return JsonResponse({"success": True})

    @staticmethod
    def parse_json(request):
        try:
            return json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON invalide."}, status=400)

    @staticmethod
    def serialize(word):
        return {
            "pk": word.pk,
            "word": word.word,
            "pronunciation_hint": word.pronunciation_hint or "",
        }


class ExerciseDetailView(LoginRequiredMixin, DictavoixAccessMixin, DetailView):
    model = DictavoixExercise
    template_name = "dictavoix/exercise_detail.html"
    context_object_name = "exercise"

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
