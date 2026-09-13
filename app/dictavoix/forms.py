from django import forms

from .models import DictavoixDictionaryWord, DictavoixSession


class DictavoixDictionaryWordForm(forms.ModelForm):
    class Meta:
        model = DictavoixDictionaryWord
        fields = ["word", "pronunciation_hint"]


class DictavoixSessionForm(forms.ModelForm):
    class Meta:
        model = DictavoixSession
        fields = [
            "error_count",
            "total_word_count",
            "dictionary_word_count",
            "notes",
        ]
        widgets = {
            "notes": forms.Textarea(
                attrs={"rows": 4, "class": "w-full rounded border-gray-300 p-2"}
            ),
        }
