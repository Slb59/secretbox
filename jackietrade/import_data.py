import yfinance as yf


class YFinanceImporter:

	def fetch_history(
		self,
		asset,
		period="1y",
		interval="1d",
	):
    
		ticker = yf.Ticker(asset.symbol)  

		df = ticker.history(  
			period=period,  
			interval=interval,  
			auto_adjust=True,  
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
				}  
			)  
	
			if created:  
				candles_created += 1  
	
		return candles_created