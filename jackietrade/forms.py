from django import forms

from .models import Asset


class MarketDataSyncForm(forms.Form):

    PERIOD_CHOICES = [
        ("1d", "1 jour"),
        ("5d", "5 jours"),
        ("1mo", "1 mois"),
        ("3mo", "3 mois"),
        ("6mo", "6 mois"),
        ("1y", "1 an"),
        ("5y", "5 ans"),
    ]

    INTERVAL_CHOICES = [
        ("1m", "1 minute"),
        ("5m", "5 minutes"),
        ("15m", "15 minutes"),
        ("1h", "1 heure"),
        ("4h", "4 heures"),
        ("1d", "1 jour"),
        ("1wk", "1 semaine"),
        ("1mo", "1 mois"),
    ]

    assets = forms.ModelMultipleChoiceField(
        queryset=Asset.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
    )

    period = forms.ChoiceField(
        choices=PERIOD_CHOICES,
        initial="1y",
    )

    interval = forms.ChoiceField(
        choices=INTERVAL_CHOICES,
        initial="1d",
    )

    def __init__(self, *args, user=None, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["assets"].queryset = Asset.objects.filter(
            watchlistitem__watchlist__user=user
        ).distinct()