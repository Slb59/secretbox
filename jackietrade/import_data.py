import yfinance as yf
import logging

from .models import Candle

logger = logging.getLogger(__name__)


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
	
			_, created = Candle.objects.get_or_create(  
				asset=asset,  
				timeframe=interval,  
				timestamp=timestamp,  

				defaults={  
					"open": row["Open"],  
					"high": row["High"],  
					"low": row["Low"],  
					"close": row["Close"],  
					"volume": row["Volume"],  
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
