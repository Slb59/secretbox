from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Div
from core.forms_helpers import action_buttons
from django.utils.translation import gettext_lazy as _

from .assetmodels import Asset
from .watchlistmodels import Watchlist, WatchlistItem


class AssetForm(forms.ModelForm):

    watchlists = forms.ModelMultipleChoiceField(
        queryset=Watchlist.objects.none(),
        required=False,
    )

    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "w-full h-64 resize-y",
            }
        ),
        required=False,
    )

    class Meta:
        model = Asset
        fields = "__all__"

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["watchlists"].queryset = (
            Watchlist.objects.filter(user=user)
        )

    def save(self, commit=True):

        asset = super().save(commit=commit)

        if commit:

            for watchlist in self.cleaned_data["watchlists"]:

                WatchlistItem.objects.get_or_create(
                    watchlist=watchlist,
                    asset=asset,
                )

        return asset

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

    SELECTION_CHOICES = [
        ("all", "Tous les assets"),
        ("selected", "Actifs sélectionnés")
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

    selection_mode = forms.ChoiceField(
        choices=SELECTION_CHOICES,
        widget=forms.RadioSelect,
        initial="selected",
    )

    watchlist = forms.ModelChoiceField(
        queryset=Watchlist.objects.none(),
        required=False,
    )


    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["period"].label = _("Période")
        self.fields["interval"].label = _("Intervalle")
        self.fields["assets"].label = _("Actifs à synchroniser")
        self.fields["selection_mode"].label = _("Mode de sélection")
        self.fields["watchlist"].label = _("Liste de surveillance")

        self.fields["assets"].queryset = Asset.objects.filter(
            watchlistitem__watchlist__user=user
        ).distinct()

        self.fields["watchlist"].queryset = Watchlist.objects.filter(user=user)

        self.helper = FormHelper()
        self.helper.form_class = "border p-8 bg-yellow-600"
        self.helper.form_method = "post"
        self.helper.form_tag = True
        self.helper.attrs = {"novalidate": "novalidate"}

        self.helper.layout = Layout(
            Div(
                Div("period", css_class="w-full md:w-1/2",),
                Div("interval", css_class="w-full md:w-1/2",),
                css_class="flex flex-col md:flex-row gap-4",
            ),
            "selection_mode",
            "watchlist",
            "assets",
            action_buttons(submit_label=_("Importer"), back_url_name="jackietrade:dashboard", back_label=_("Retour")),
        )