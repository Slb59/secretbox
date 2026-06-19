from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TradingSettings(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="watchlists",
    )

    risk_budget = 2000