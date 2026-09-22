import json

from devapps.models import DevappsAction, DevappsApplication, DevappsVersion
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DevappsDashboardTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="devapps@example.com", password="password"
        )
        self.application = DevappsApplication.objects.create(name="SecretBox")
        self.version = DevappsVersion.objects.create(name="0.1.0")
        self.client.force_login(self.user)

    def test_dashboard_and_action_api_support_crud(self):
        dashboard_url = reverse("devapps:dashboard")
        api_url = reverse("devapps:actions_api")
        response = self.client.get(dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SecretBox")
        self.assertContains(response, "0.1.0")

        payload = {
            "application": self.application.pk,
            "version": self.version.pk,
            "category": "analysis",
            "description": "Documenter le déploiement",
            "details": "Ajouter les étapes.",
            "priority": 50,
            "state": "todo",
            "estimated_time": 30,
            "planned": True,
        }
        response = self.client.post(
            api_url, data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        action_pk = response.json()["pk"]

        payload.update({"pk": action_pk, "state": "done"})
        response = self.client.patch(
            api_url, data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["state"], "done")

        response = self.client.delete(
            api_url,
            data=json.dumps({"pk": action_pk}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(DevappsAction.objects.filter(pk=action_pk).exists())

    def test_dashboard_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("devapps:dashboard"))
        self.assertEqual(response.status_code, 302)
