from django import forms
from django.utils.translation import gettext_lazy as _
from .memo import Memo

class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = [
            "state",
            "duration",
            "description",
            "appointment",
            "category",
            "who",
            "place",
            "periodic",
            "planned_date",
            "priority",
            "note",
        ]

    def __init__(self, *args, user=None, instance=None, **kwargs):
        super().__init__(*args, instance=instance, **kwargs)

        self.fields["state"].label = _("État")
        self.fields["duration"].label = _("Durée")
        self.fields["description"].label = _("Description")
        self.fields["appointment"].label = _("Rdv")
        self.fields["category"].label = _("Catégorie")
        self.fields["who"].label = _("Personnes")
        self.fields["place"].label = _("Lieu")
        self.fields["periodic"].label = _("Fréquence")

        # Resize the state field
        Field("state", wrapper_class="w-full sm:w-[150px]")
        # Resize the duration field
        self.fields["duration"].widget.field_class = "w-full sm:w-[90px]"
        self.fields["who"].widget = forms.CheckboxSelectMultiple()

        print(user)
        if instance and user and instance.can_edit_limited(user):
            for name, field in self.fields.items():
                if name not in ["state", "priority"]:
                    field.disabled = True
                    Field(name, wrapper_class="readonly")
                    if name == "who":
                        field.widget.attrs["disabled"] = True
                    #         field.widget.attrs.update({"class": "readonly text-gray-500 pointer-events-none"})
                else:
                    Field(name, wrapper_class="editable")
                #         field.widget.attrs.update({"class": "editable"})

        self.helper = FormHelper()
        self.helper.form_class = "border p-8"
        self.helper.form_method = "post"
        self.helper.form_tag = True
        self.helper.attrs = {"novalidate": "novalidate"}

        self.helper.layout = Layout(
            "state",
            "duration",
            "description",
            "appointment",
            "category",
            "who",
            "place",
            "periodic",
            "planned_date",
            "priority",
            "note",
            action_buttons(back_url_name="home", back_label="Liste"),
        )