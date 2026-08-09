import yfinance as yf
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from jackietrade.assetmodels import Asset
from jackietrade.import_data import YFinanceImporter


class Command(BaseCommand):
    help = "Affiche les données Yahoo Finance d'un actif"

    def add_arguments(self, parser):

        parser.add_argument(
            "symbol",
            type=str,
            help="Symbole Yahoo Finance",
        )

    def handle(self, *args, **options):

        symbol = options["symbol"].upper()

        asset = get_object_or_404(Asset, symbol=symbol)

        self.stdout.write(f"Chargement de {asset.name}")

        importer = YFinanceImporter()

        ticker = yf.Ticker(asset.symbol)

        df = ticker.history(
            period="1mo",
            interval="1d",
        )

        self.stdout.write(self.style.SUCCESS(f"{len(df)} lignes récupérées"))

        self.stdout.write(str(df))

        self.stdout.write("Chargement des données dans la base de données")

        count = importer.import_history(
            asset=asset,
            period="1mo",
            interval="1d",
        )

        self.stdout.write(self.style.SUCCESS(f"{count} candles créées"))

        # self.stdout.write(asset.candles)
