from django.db import models
from django.core.validators import (MinValueValidator, MaxValueValidator,)
from decimal import Decimal

from .assetmodels import Asset
from .settingsmodels import TradingSettings


class TradeJournalEntry(models.Model):

    class ConfidenceLevel(models.IntegerChoices):
        VERY_LOW = 1, "Très faible"
        LOW = 2, "Faible"
        MEDIUM = 3, "Moyenne"
        HIGH = 4, "Haute"
        VERY_HIGH = 5, "Très haute"


    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    session_date = models.DateField()
    
    # pour mettre un resumé de la session
    title = models.CharField(max_length=200,)
    
    reviewed_at = models.DateTimeField(null=True, blank=True,)

    

	# mettre en literraire les observations et ensuite expliquer un plan
	# d'action avec des hypothèses sur l'avenir en fonction de 
	# l'actualité économique
    # exemple : RSI 14 : 72, Cours au-dessus de la MM20 et MM50.
    # Volume supérieur à la moyenne. Résistance à 72€.
    analysis_notes = models.TextField(blank=True,)

	# dire j'achète x actions à ... avec un stop_loss...
    execution_notes = models.TextField(
        blank=True,
    )

    entry_price = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True,
    )

    stop_loss = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True,
    )

    take_profit = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True,
    )

	# après revue: mettre j'aurai pas du faire ca, ou l'hypothèse est
	# bonne ...
    result_notes = models.TextField(
        blank=True,
    )
   
    # niveau de confiance dans la décision de 1 à 5
    confidence_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    snapshots = models.ManyToManyField(
        IndicatorSnapshot,
        blank=True,
	)
	
	def __str__(self):  
  
	    return (  
	        f"{self.session_date} - "  
	        f"{self.asset.symbol}"  
	    )
    
    @property
    def quantity(self):

        if not self.entry_price:
            return 0

        settings = TradingSettings()
        return int(settings.risk_budget / self.entry_price)

    @property
    def invested_amount(self):
        return self.quantity * self.entry_price
    
    @property
    def potential_profit(self):
        return self.quantity * (self.take_profit - self.entry_price)
    
    @property
    def potential_loss(self):
        return self.quantity * (self.entry_price - self.stop_loss)
    


class TradeJournalScreenshot(models.Model):

    journal_entry = models.ForeignKey(
        "TradeJournalEntry",
        on_delete=models.CASCADE,
        related_name="screenshots",
    )

    image = models.ImageField(
        upload_to="trade_journal/",
    )

    caption = models.CharField(
        max_length=200,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )