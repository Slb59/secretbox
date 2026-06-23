"""Filter forms used to refine the results displayed to the user.

Contains optional fields allowing you to dynamically filter database objects.
"""

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .choices import (
    CATEGORY_CHOICES,
    PERIODIC_CHOICES,
    PLACE_CHOICES,
    PRIORITY_CHOICES,
)
from .memo import Memo

Member = get_user_model()


class MemoFilterForm(forms.Form):
    state = forms.ChoiceField(
        choices=[("", "Tous")] + Memo.STATE_CHOICES, required=False, label="Etat"
    )
    duration_min = forms.IntegerField(required=False, min_value=0, label="Durée min")
    duration_max = forms.IntegerField(required=False, min_value=0, label="Durée max")
    description = forms.CharField(required=False)
    appointment = forms.ChoiceField(
        choices=[("", "Tous")] + Memo.APPOINTEMENT_CHOICES,
        required=False,
        label=_("Rendez-vous"),
    )
    category = forms.ChoiceField(
        choices=[("", "Toutes")] + CATEGORY_CHOICES,
        required=False,
        label=_("Catégorie"),
    )
    who = forms.ModelChoiceField(
        queryset=Member.objects.all().order_by("trigram"),
        required=False,
        label=_("Qui"),
        empty_label="Tous",
    )
    place = forms.ChoiceField(
        choices=[("", "Toutes")] + PLACE_CHOICES, required=False, label=_("Lieu")
    )
    periodic = forms.ChoiceField(
        choices=[("", "Toutes")] + PERIODIC_CHOICES,
        required=False,
        label=_("Fréquence"),
    )
    planned_date_start = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label=_("Date de planification"),
    )
    planned_date_end = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"}), label=_("_")
    )
    priority = forms.ChoiceField(
        choices=[("", "Toutes")] + PRIORITY_CHOICES, required=False, label=_("Priorité")
    )
    done_date_start = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label=_("Date de validation"),
    )
    done_date_end = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"}), label=_("_")
    )
    note = forms.CharField(required=False)
    done_date_isnull = forms.BooleanField(
        required=False, label="Sans date de validation"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.form_class = "p-4 bg-amber-300 rounded mb-4"
        self.helper.label_class = "font-semibold"
        self.helper.field_class = "w-full"
        self.helper.attrs = {
            "id": "memo-filter-form",
            "novalidate": "novalidate",
            "data-autosubmit": "true",
        }

        self.helper.layout = Layout(
            Row(
                Column("state", css_class="sm:col-span-1"),
                Column("duration_min", css_class="sm:col-span-1"),
                Column("duration_max", css_class="sm:col-span-1"),
                Column("description", css_class="sm:col-span-3"),
                Column("appointment", css_class="sm:col-span-1"),
                Column("category", css_class="sm:col-span-1"),
                Column("who", css_class="sm:col-span-1"),
                Column("place", css_class="sm:col-span-1"),
                Column("periodic", css_class="sm:col-span-1"),
                css_class="grid grid-cols-11 gap-4",
            ),
            Row(
                Column("planned_date_start", css_class="sm:col-span-1"),
                Column("planned_date_end", css_class="sm:col-span-1"),
                Column("priority", css_class="sm:col-span-1"),
                Column("done_date_start", css_class="sm:col-span-1"),
                Column("done_date_end", css_class="sm:col-span-1"),
                Column("done_date_isnull", css_class="sm:col-span-1"),
                css_class="grid grid-cols-5 gap-4 py-2",
            ),
        )
