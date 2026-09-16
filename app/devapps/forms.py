from django import forms

from .models import DevappsAction


class DevappsActionForm(forms.ModelForm):
    class Meta:
        model = DevappsAction
        fields = [
            "application",
            "version",
            "category",
            "description",
            "details",
            "priority",
            "state",
            "estimated_time",
            "achieved_time",
            "started_at",
            "finished_at",
            "planned",
        ]
        widgets = {
            "details": forms.Textarea(attrs={"rows": 3}),
            "started_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "finished_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
