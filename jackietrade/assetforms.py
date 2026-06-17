from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from core.forms_helpers import action_buttons
from .models import Asset


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ["symbol", "code", "name", "asset_type", "sector", "exchange", "is_active"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["symbol"].label = _("Symbole Yahoo Finance")
        self.fields["code"].label = _("Code TradingView")
        self.fields["name"].label = _("Nom de l'actif")
        self.fields["asset_type"].label = _("Type d'actif")
        self.fields["sector"].label = _("Secteur")
        self.fields["exchange"].label = _("Bourse")
        self.fields["is_active"].label = _("Actif")

        self.helper = FormHelper()
        self.helper.form_class = "border p-8 bg-yellow-600"
        self.helper.form_method = "post"
        self.helper.form_tag = True
        self.helper.attrs = {"novalidate": "novalidate"}

        self.helper.layout = Layout(
            "symbol",
            "code",
            "name",
            "asset_type",
            "sector",
            "exchange",
            "is_active",
            action_buttons(back_url_name="jackietrade:asset_list")
        )
