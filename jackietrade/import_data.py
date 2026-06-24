import logging
from decimal import Decimal

import yfinance as yf
from django.utils import timezone

from .assetmodels import Candle

logger = logging.getLogger(__name__)


def to_decimal(value):
    return Decimal(str(value))


class YFinanceImporter:
    def import_history(
        self,
        asset,
        period="1y",
        interval="1d",
    ):

        logger.info(
            "Début import %s (period=%s interval=%s)",
            asset.symbol,
            period,
            interval,
        )

        ticker = yf.Ticker(asset.symbol)

        df = ticker.history(
            period=period,
            interval=interval,
            auto_adjust=True,
        )

        if df.empty:
            logger.warning(
                "%s : aucune donnée retournée",
                asset.symbol,
            )
        else:
            logger.info(
                "%s : %s lignes récupérées",
                asset.symbol,
                len(df),
            )

        candles_created = 0

        for timestamp, row in df.iterrows():
            timestamp = timestamp.to_pydatetime()

            if timezone.is_naive(timestamp):
                timestamp = timezone.make_aware(timestamp)

            _, created = Candle.objects.get_or_create(
                asset=asset,
                timeframe=interval,
                timestamp=timestamp,
                defaults={
                    "open": to_decimal(row["Open"]),
                    "high": to_decimal(row["High"]),
                    "low": to_decimal(row["Low"]),
                    "close": to_decimal(row["Close"]),
                    "volume": to_decimal(row["Volume"]),
                },
            )

            if created:
                candles_created += 1

        logger.info(
            "%s : %s nouvelles candles",
            asset.symbol,
            candles_created,
        )

        return candles_created
