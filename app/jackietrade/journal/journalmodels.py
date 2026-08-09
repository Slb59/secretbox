from django.contrib.auth import get_user_model
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..assetmodels import Asset
from ..settingsmodels import TradingSettings

User = get_user_model()


class TradeJournalEntry(models.Model):
    class ConfidenceLevel(models.IntegerChoices):
        VERY_LOW = 1, _("Très faible")
        LOW = 2, _("Faible")
        MEDIUM = 3, _("Moyenne")
        HIGH = 4, _("Haute")
        VERY_HIGH = 5, _("Très haute")

    class ExitReason(models.TextChoices):
        STOP_LOSS = "stop_loss", _("Stop Loss")
        TAKE_PROFIT = "take_profit", _("Take Profit")
        OPEN = "open", _("Position ouverte")

    class Status(models.TextChoices):
        DRAFT = "draft", _("Préparation")
        WATCHING = "watching", _("Sous surveillance")
        OPEN = "open", _("Position ouverte")
        CLOSED = "closed", _("Position clôturée")
        CANCELLED = "cancelled", _("Scénario abandonné")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="journals",
        default=1,
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    session_date = models.DateField()

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    # mettre en literraire les observations et ensuite expliquer un plan
    # d'action avec des hypothèses sur l'avenir en fonction de
    # l'actualité économique
    # exemple : RSI 14 : 72, Cours au-dessus de la MM20 et MM50.
    # Volume supérieur à la moyenne. Résistance à 72€.
    observation_notes = models.TextField(
        blank=True,
    )
    # dire en quoi l'actualité peut influencer le marché
    # guerre, annonce présidentielle ...
    market_context = models.TextField(
        blank=True,
    )

    planned_entry_price = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True,
    )

    planned_stop_loss = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True,
    )

    planned_take_profit = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True,
    )

    # niveau de confiance dans la décision de 1 à 5
    confidence_level = models.IntegerField(
        choices=ConfidenceLevel.choices, blank=True, null=True
    )

    # dire j'achète x actions à ... avec un stop_loss...
    execution_notes = models.TextField(
        blank=True,
    )

    entry_order_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    entry_quantity = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(2000)],
    )
    entry_price_executed = models.DecimalField(
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

    exit_order_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    exit_quantity = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(2000)],
    )
    exit_price = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True,
    )

    exit_reason = models.CharField(
        max_length=20,
        choices=ExitReason.choices,
        blank=True,
        default=ExitReason.OPEN,
    )

    def __str__(self):

        return f"{self.session_date} - {self.asset.symbol}"

    @property
    def quantity(self):

        settings = TradingSettings.objects.first()

        if not self.entry_price or not settings.risk_budget:
            return 0

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

    @property
    def risk_reward_ratio(self):

        if not self.entry_price or not self.stop_loss or not self.take_profit:
            return None

        risk = self.entry_price - self.stop_loss
        reward = self.take_profit - self.entry_price

        if reward <= 0:
            return None

        return round(risk / reward, 2)


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


class Analysis:
    @staticmethod
    def compute(entry): ...
