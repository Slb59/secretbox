from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from core.forms_helpers import action_buttons
from .models import Watchlist


class WatchlistForm(forms.ModelForm):

    class Meta:
        model = Watchlist
        fields = ["name", "is_default"]
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["name"].label = _("Nom de la liste de suivi")
        self.fields["is_default"].label = _("Définir comme liste de suivi par défaut")

        self.helper = FormHelper()
        self.helper.form_class = "border p-8 bg-yellow-600"
        self.helper.form_method = "post"
        self.helper.form_tag = True
        self.helper.attrs = {"novalidate": "novalidate"}

        self.helper.layout = Layout(
            "name", 
            "is_default",
            action_buttons(back_url_name="jackietrade:dashboard", back_label=_("Retour"))
        )