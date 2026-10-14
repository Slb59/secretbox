from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import SamiCategory, SamiDay, SamiEntry, SamiIndicator


class SamiDashboardOrderingTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            email="samicheck@example.com", password="password"
        )
        self.client.force_login(user)

    def test_indicator_columns_follow_saved_category_and_indicator_order(self):
        later_category = SamiCategory.objects.create(name="Later", display_order=2)
        earlier_category = SamiCategory.objects.create(name="Earlier", display_order=1)
        SamiIndicator.objects.create(
            category=later_category, title="First", display_order=1
        )
        SamiIndicator.objects.create(
            category=later_category, title="Second", display_order=2
        )
        SamiIndicator.objects.create(
            category=earlier_category, title="Indicator", display_order=1
        )

        response = self.client.get(reverse("samicheck:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [column["title"] for column in response.context["table_columns"]],
            ["Earlier - Indicator", "Later - First", "Later - Second"],
        )

    def test_create_day_saves_date_and_indicator_values(self):
        category = SamiCategory.objects.create(name="Health")
        indicator = SamiIndicator.objects.create(
            category=category, title="Sleep", max_level=4
        )

        response = self.client.post(
            reverse("samicheck:create_day"),
            data={"date": "2026-10-14", f"indicator_{indicator.pk}": "3"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        day = SamiDay.objects.get(date="2026-10-14")
        self.assertEqual(SamiEntry.objects.get(day=day, indicator=indicator).value, 3)
        self.assertEqual(response.json()["row"][f"indicator_{indicator.pk}"], 3)

    def test_create_day_rejects_values_above_indicator_maximum(self):
        category = SamiCategory.objects.create(name="Health")
        indicator = SamiIndicator.objects.create(
            category=category, title="Sleep", max_level=4
        )

        response = self.client.post(
            reverse("samicheck:create_day"),
            data={"date": "2026-10-14", f"indicator_{indicator.pk}": "5"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(SamiDay.objects.exists())
