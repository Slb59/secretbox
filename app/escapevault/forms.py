"""Defines forms based on the application's templates.
Used for creating and updating objects via views
"""

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout
from django import forms
from django.utils.translation import gettext_lazy as _

from core.forms_helpers import action_buttons

from .models import NomadePosition


class EscapeVaultForm(forms.ModelForm):
    new_review = forms.CharField(
        label=_("Ajouter un avis"),
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )

    class Meta:
        model = NomadePosition
        fields = [
            "name",
            "category",
            "city",
            "country",
            "latitude",
            "longitude",
            "link_to_site",
            "opening_date",
            "closing_date",
            "stars",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].label = _("Nom de la position")
        self.fields["stars"].label = _("Etoiles")
        self.fields["category"].label = _("Catégorie")
        self.fields["city"].label = _("Ville")
        self.fields["country"].label = _("Pays")
        self.fields["latitude"].label = _("Latitude")
        self.fields["longitude"].label = _("Longitude")
        self.fields["link_to_site"].label = _("Lien vers le site internet")
        self.fields["opening_date"].label = _("Date d'ouverture")
        self.fields["closing_date"].label = _("Date de fermeture")

        # Resize the city and country field
        self.fields["city"].widget.attrs.update(
            {"class": "h-full sm:h-[60px]", "style": "max-height: 40px;"}
        )

        self.fields["country"].widget.attrs.update(
            {"class": "h-full sm:h-[60px]", "style": "max-height: 40px;"}
        )

        self.helper = FormHelper()
        self.helper.form_class = "border p-8"

        self.helper.layout = Layout(
            Div(
                Div("name", css_class="w-full sm:col-span-3"),
                Div("stars", css_class="w-full sm:col-span-1"),
                Div("category", css_class="w-full sm:col-span-2"),
                css_class="grid grid-cols-6 gap-4",
            ),
            # "category",
            Div(
                Div("city", css_class="w-full sm:sm:col-span-3"),
                Div("country", css_class="w-full sm:col-span-2"),
                css_class="grid grid-cols-5 gap-4",
            ),
            Div(
                Div("latitude", css_class="w-full sm:col-span-2"),
                Div("longitude", css_class="w-full sm:col-span-2"),
                css_class="grid grid-cols-5 gap-4",
            ),
            "link_to_site",
            Div(
                Div("opening_date", css_class="w-full sm:col-span-2"),
                Div("closing_date", css_class="w-full sm:col-span-2"),
                css_class="grid grid-cols-5 gap-4",
            ),
            action_buttons(
                back_url_name="escapevault:list_positions", back_label="Liste"
            ),
        )

        # Insert the new_review field at the end of the form,
        # just before the submit button
        self.helper.layout.fields.insert(-1, "new_review")
