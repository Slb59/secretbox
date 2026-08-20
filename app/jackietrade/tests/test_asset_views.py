from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from app.jackietrade.assetmodels import Asset, Sector

User = get_user_model()


class AssetListViewTests(TestCase):
    """test:
    L'accès authentifié/non authentifié.
    Le contenu du contexte.
    Le filtrage des actifs actifs/inactifs.
    Le regroupement par secteur.
    La modification d'un actif.
    """

    def setUp(self):

        self.user = User.objects.create_user(
            email="testuser@test.com",
            password="secret",
        )

        self.bank_sector = Sector.objects.create(
            code="BANK",
            name="Banque",
        )

        self.auto_sector = Sector.objects.create(
            code="AUTO",
            name="Automobile",
        )

        self.asset1 = Asset.objects.create(
            symbol="BNP.PA",
            name="BNP Paribas",
            asset_type="stock",
            sector=self.bank_sector,
            is_active=True,
        )

        self.asset2 = Asset.objects.create(
            symbol="GLE.PA",
            name="Société Générale",
            asset_type="stock",
            sector=self.bank_sector,
            is_active=True,
        )

        self.asset3 = Asset.objects.create(
            symbol="RNO.PA",
            name="Renault",
            asset_type="stock",
            sector=self.auto_sector,
            is_active=True,
        )

        self.inactive_asset = Asset.objects.create(
            symbol="OLD.PA",
            name="Inactive",
            asset_type="stock",
            sector=self.auto_sector,
            is_active=False,
        )

    def test_login_required(self):

        response = self.client.get(reverse("jackietrade:asset_list"))

        self.assertEqual(response.status_code, 302)

    def test_asset_list_page(self):

        self.client.login(
            username="testuser",
            password="secret",
        )

        response = self.client.get(reverse("jackietrade:asset_list"))

        self.assertEqual(response.status_code, 200)

    def test_only_active_assets_are_returned(self):

        self.client.login(
            username="testuser",
            password="secret",
        )

        response = self.client.get(reverse("jackietrade:asset_list"))

        assets = response.context["assets"]

        self.assertEqual(assets.count(), 3)

        self.assertNotIn(
            self.inactive_asset,
            assets,
        )

    def test_grouped_assets(self):

        self.client.login(
            username="testuser",
            password="secret",
        )

        response = self.client.get(reverse("jackietrade:asset_list"))

        grouped_assets = response.context["grouped_assets"]

        self.assertEqual(len(grouped_assets), 2)

        self.assertEqual(
            grouped_assets[0]["sector"],
            self.auto_sector,
        )

        self.assertEqual(
            grouped_assets[1]["sector"],
            self.bank_sector,
        )

    def test_sectors_in_context(self):

        self.client.login(
            username="testuser",
            password="secret",
        )

        response = self.client.get(reverse("jackietrade:asset_list"))

        sectors = response.context["sectors"]

        self.assertEqual(
            sectors.count(),
            2,
        )


class AssetUpdateViewTests(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            email="testuser@test.com",
            password="secret",
        )

        self.sector = Sector.objects.create(
            code="BANK",
            name="Banque",
        )

        self.asset = Asset.objects.create(
            symbol="BNP.PA",
            name="BNP Paribas",
            asset_type="stock",
            sector=self.sector,
        )

    def test_login_required(self):

        response = self.client.get(
            reverse(
                "jackietrade:asset_update",
                args=[self.asset.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_update_page_is_displayed(self):

        self.client.login(
            email="testuser@test.com",
            password="secret",
        )

        response = self.client.get(
            reverse(
                "jackietrade:asset_update",
                args=[self.asset.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_update_asset(self):

        self.client.login(
            email="testuser@test.com",
            password="secret",
        )

        response = self.client.post(
            reverse(
                "jackietrade:asset_update",
                args=[self.asset.pk],
            ),
            {
                "symbol": "BNP.PA",
                "name": "BNP Paribas Modifié",
                "asset_type": "stock",
                "sector": self.sector.pk,
                "currency": "EUR",
                "is_active": True,
            },
        )

        print(response.status_code)
        print(response.context["form"].errors)
        print(response.content)

        self.assertRedirects(
            response,
            reverse("jackietrade:asset_list"),
        )

        self.asset.refresh_from_db()

        self.assertEqual(
            self.asset.name,
            "BNP Paribas Modifié",
        )
