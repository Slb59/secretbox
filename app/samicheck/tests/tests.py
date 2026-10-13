from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import SamiCategory, SamiIndicator


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
