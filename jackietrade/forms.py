from django import forms

from .models import Asset


class MarketDataSyncForm(forms.Form):

// 1d 5d 1mo 3mo 6mo 1y 5y max
    PERIOD_CHOICES = [
        ("1mo", "1 mois"),
        ("3mo", "3 mois"),
        ("6mo", "6 mois"),
        ("1y", "1 an"),
        ("5y", "5 ans"),
    ]

// 1m 5m 15m 1h 1d 1wk 1mo
    INTERVAL_CHOICES = [
        ("1d", "1 jour"),
        ("1h", "1 heure"),
        ("4h", "4 heures"),
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