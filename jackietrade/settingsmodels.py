from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TradingSettings(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="trading_settings",
    )

    risk_budget = 2000
