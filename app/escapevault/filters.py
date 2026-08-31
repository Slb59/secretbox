"""Filter forms used to refine the results displayed to the user.

Contains optional fields allowing you to dynamically filter database objects.
"""

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import NomadePosition


class EscapeVaultFilterForm(forms.Form):
    category = forms.ChoiceField(
        choices=[("", "Toutes")] + NomadePosition.CATEGORY_CHOICES,
        required=False,
        label=_("Catégorie"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.form_class = "p-4 rounded mb-4"
        self.helper.label_class = "font-semibold"
        self.helper.field_class = "w-full"
        self.helper.attrs = {
            "id": "ev-filter-form",
            "novalidate": "novalidate",
            "data-autosubmit": "true",
        }

        self.helper.layout = Layout(
            Row(
                Column("category", css_class="sm:col-span-1"),
                css_class="grid grid-cols-5 gap-4",
            ),
        )
