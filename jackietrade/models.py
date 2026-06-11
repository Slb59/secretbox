from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db.models import Q


User = get_user_model()


class Sector(models.Model):

    code = models.CharField(
        max_length=4,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z]{4}$",
                message="Le code doit contenir exactement 4 lettres."
            )
        ],
    )

    name = models.CharField(
        max_length=100,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(code__regex=r"[A-Z]{4}$"),
                name="sector_code_four_uppercase_letters",
            )
        ]


    def __str__(self):
        return self.name

    def clean(self):
        super().clean()

        if self.code:
            self.code = self.code.upper()

    def save(self, *args, **kwargs):
        if self.code:
            self.code = self.code.upper()
        super().save(*args, **kwargs)

class Exchange(models.Model):

    code = models.CharField(
        max_length=20,
        unique=True,
    )

    name = models.CharField(
        max_length=100,
    )

    country = models.CharField(
        max_length=50,
    )

    timezone = models.CharField(
        max_length=50,
    )

    open_time_utc = models.TimeField()

    close_time_utc = models.TimeField()

    def __str__(self):
        return self.name

class Asset(models.Model):

    class AssetType(models.TextChoices):
        STOCK = "stock", "Stock"
        ETF = "etf", "ETF"
        CRYPTO = "crypto", "Crypto"
        FOREX = "forex", "Forex"
    

    symbol = models.CharField(
        max_length=20,
        unique=True,
    )

    name = models.CharField(max_length=255)

    asset_type = models.CharField(
        max_length=20,
        choices=AssetType.choices,
    )
    
    sector = models.ForeignKey(  
		Sector,  
		on_delete=models.SET_NULL,  
		null=True,  
		blank=True,  
	)

    exchange = models.ForeignKey(  
		Exchange,  
		on_delete=models.SET_NULL,  
		null=True,  
	)

    currency = models.CharField(
        max_length=10,
        default="EUR",
    )

    web_site = models.URLField(
        max_length=255,
        null=True,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Notes"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    last_sync_at = models.DateTimeField(
    null=True,
    blank=True,
	)

    def __str__(self):
        return self.symbol

class Watchlist(models.Model):  
  
    user = models.ForeignKey(  
    User,  
    on_delete=models.CASCADE,  
    )  
    
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}" 

class WatchlistItem(models.Model):  
  
	watchlist = models.ForeignKey(  
	Watchlist,  
	on_delete=models.CASCADE,  
	)

	asset = models.ForeignKey(  
	Asset,  
	on_delete=models.CASCADE,  
	)  
	  
	added_at = models.DateTimeField(auto_now_add=True)

class Candle(models.Model):

    class Timeframe(models.TextChoices):
        DAY_1 = "1d", "1 Day"
        HOUR_4 = "4h", "4 Hours"
        HOUR_1 = "1h", "1 Hour"

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="candles",
    )

    timeframe = models.CharField(
        max_length=10,
        choices=Timeframe.choices,
    )

    timestamp = models.DateTimeField()

    open = models.DecimalField(max_digits=20, decimal_places=8)
    high = models.DecimalField(max_digits=20, decimal_places=8)
    low = models.DecimalField(max_digits=20, decimal_places=8)
    close = models.DecimalField(max_digits=20, decimal_places=8)

    volume = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        unique_together = (
            "asset",
            "timeframe",
            "timestamp",
        )

        indexes = [
            models.Index(fields=[
                "asset",
                "timeframe",
                "timestamp",
            ])
        ]