from unittest.mock import patch

import pandas as pd
from django.test import TestCase

from jackietrade.assetmodels import Asset, Candle, Sector
from jackietrade.import_data import YFinanceImporter


class YFinanceImporterTests(TestCase):
    def setUp(self):

        self.sector = Sector.objects.create(code="FINA", name="Finance")

        self.asset = Asset.objects.create(
            symbol="BNP Paribas S.A. Class A",
            name="BNP Paribas S.A. Class A",
            asset_type="stock",
            sector=self.sector,
        )

        self.df = pd.DataFrame(
            {
                "Open": [100, 101],
                "High": [105, 106],
                "Low": [99, 100],
                "Close": [104, 105],
                "Volume": [1000, 2000],
            },
            index=pd.to_datetime(
                [
                    "2026-01-01",
                    "2026-01-02",
                ]
            ),
        )

        self.importer = YFinanceImporter()

    @patch("jackietrade.import_data.yf.Ticker")
    def test_import_creates_candles(self, mock_ticker):
        mock_ticker.return_value.history.return_value = self.df
        created = self.importer.import_history(self.asset)
        self.assertEqual(created, 2)
        self.assertEqual(
            Candle.objects.count(),
            2,
        )

    @patch("jackietrade.import_data.yf.Ticker")
    def test_import_is_idempotent(self, mock_ticker):
        mock_ticker.return_value.history.return_value = self.df
        created = self.importer.import_history(self.asset)
        created = self.importer.import_history(self.asset)
        self.assertEqual(created, 0)
        self.assertEqual(Candle.objects.count(), 2)
