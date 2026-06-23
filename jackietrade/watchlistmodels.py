from django.contrib.auth import get_user_model
from django.db import models

from .assetmodels import Asset

User = get_user_model()


class Watchlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="watchlists",
    )

    name = models.CharField(max_length=100)

    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.is_default:
            Watchlist.objects.filter(user=self.user, is_default=True).exclude(
                pk=self.pk
            ).update(is_default=False)

    def add_asset(self, asset):
        WatchlistItem.objects.get_or_create(watchlist=self, asset=asset)

    def remove_asset(self, asset):
        WatchlistItem.objects.filter(watchlist=self, asset=asset).delete()


class WatchlistItem(models.Model):
    watchlist = models.ForeignKey(
        Watchlist,
        on_delete=models.CASCADE,
        related_name="assets",
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="watchlists",
    )

    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["watchlist", "asset"], name="unique_asset_per_watchlist"
            )
        ]
        indexes = [
            models.Index(fields=["watchlist", "asset"]),
        ]
