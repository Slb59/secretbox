from django import forms

from .assetmodels import Asset


class AssetAdminForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = "__all__"

        widgets = {
            "notes": forms.Textarea(
                attrs={
                    "rows": 10,
                    "cols": 80,
                }
            ),
        }
