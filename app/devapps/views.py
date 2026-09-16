# Create your views here.
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from .choices import Category, State
from .forms import DevappsActionForm
from .models import DevappsAction, DevappsApplication, DevappsVersion


class DevappsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "devapps-dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "applications": list(
                    DevappsApplication.objects.order_by("name").values("pk", "name")
                ),
                "versions": list(
                    DevappsVersion.objects.order_by("name").values("pk", "name")
                ),
                "categories": [
                    {"value": value, "label": label}
                    for value, label in Category.choices
                ],
                "states": [
                    {"value": value, "label": label} for value, label in State.choices
                ],
            }
        )
        return context


class DevappsActionAPIView(LoginRequiredMixin, View):
    def get(self, request):
        actions = DevappsAction.objects.select_related("application", "version")
        return JsonResponse([self.serialize(action) for action in actions], safe=False)

    def post(self, request):
        data = self.parse_json(request)
        if isinstance(data, JsonResponse):
            return data
        form = DevappsActionForm(data)
        if not form.is_valid():
            return JsonResponse({"errors": form.errors}, status=400)
        return JsonResponse(self.serialize(form.save()), status=201)

    def patch(self, request):
        data = self.parse_json(request)
        if isinstance(data, JsonResponse):
            return data
        action = get_object_or_404(DevappsAction, pk=data.get("pk"))
        form = DevappsActionForm(data, instance=action)
        if not form.is_valid():
            return JsonResponse({"errors": form.errors}, status=400)
        return JsonResponse(self.serialize(form.save()))

    def delete(self, request):
        data = self.parse_json(request)
        if isinstance(data, JsonResponse):
            return data
        action = get_object_or_404(DevappsAction, pk=data.get("pk"))
        action.delete()
        return JsonResponse({"success": True})

    @staticmethod
    def serialize(action):
        started_at = (
            timezone.localtime(action.started_at) if action.started_at else None
        )
        return {
            "pk": action.pk,
            "application": action.application_id,
            "application_name": action.application.name,
            "version": action.version_id,
            "version_name": action.version.name if action.version else "",
            "category": action.category,
            "description": action.description,
            "details": action.details,
            "priority": action.priority,
            "state": action.state,
            "estimated_time": action.estimated_time,
            "achieved_time": action.achieved_time,
            "started_at": started_at.isoformat() if started_at else "",
            "finished_at": action.finished_at.isoformat() if action.finished_at else "",
            "planned": action.planned,
        }

    @staticmethod
    def parse_json(request):
        try:
            return json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON invalide."}, status=400)
