from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.utils.translation import gettext_lazy as _

from core.forms_helpers import action_buttons

from .journalmodels import TradeJournalEntry


class JournalHeaderForm(forms.ModelForm):
    class Meta:
        model = TradeJournalEntry
        fields = ["session_date", "asset"]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["session_date"].label = _("Date de session")
        self.fields["asset"].label = _("Choix de l'actif")

        self.helper = FormHelper()
        self.helper.form_class = "border p-8 bg-yellow-600"
        self.helper.form_method = "post"
        self.helper.form_tag = True
        self.helper.attrs = {"novalidate": "novalidate"}

        self.helper.layout = Layout(
            "session_date",
            "asset",
            action_buttons(back_url_name="jackietrade:journal_list"),
        )
