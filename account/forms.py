#account/forms.py


# from django.contrib.auth.models import User



# class UserRegisterForm(forms.ModelForm):
#     password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Confirmer le mot de passe', widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['username', 'email']
    
#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password1'] != cd['password2']:
#             raise forms.ValidationError("Les mots de passe ne correspondent pas")
#         return cd['password2']

# ----



from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Submit
from django import forms
from django.contrib.auth import authenticate, forms as auth_forms, get_user_model
from django.contrib.auth.forms import (
    PasswordResetForm as DjangoPasswordResetForm,
    UserChangeForm,
)
from django.utils.translation import gettext_lazy as _

MyUser = get_user_model()

from .models import MemberProfile


class LoginForm(auth_forms.AuthenticationForm):

    username = forms.EmailField(
        label=_("Identifiant"),
        widget=forms.EmailInput(
            attrs={
                "placeholder": _("Votre adresse email"),
                "class": "form-input",
                "autofocus": True,
            }
        ),
    )

    password = forms.CharField(
        label=_("Mot de passe"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"placeholder": _("Votre mot de passe"), "class": "form-input"}
        ),
    )



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "mt-4"

        self.helper.layout = Layout(
            "username",
            "password",
            Submit(
                "submit",
                "Se connecter",
                css_class="button-valider",
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_("Email ou mot de passe incorrect"))

        return cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("This account is inactive."),
                code="inactive",
            )

    def get_user(self):
        return getattr(self, "user_cache", None)


class MyUserCreationForm(auth_forms.UserCreationForm):
    """New Member Creation Form"""

    class Meta(auth_forms.UserCreationForm):
        model = MyUser
        fields = {"trigram", "email", "password"}


class MyUserChangeForm(auth_forms.UserChangeForm):
    """New Member Creation Form"""

    class Meta(auth_forms.UserChangeForm):
        model = MyUser
        fields = {"trigram", "email", "password"}


class ProfileUpdateForm(UserChangeForm):
    email = forms.EmailField(
        label=_("Email"), widget=forms.EmailInput(attrs={"class": "form-input"})
    )
    trigram = forms.CharField(
        label=_("Trigram"),
        max_length=5,
        widget=forms.TextInput(attrs={"class": "form-input"}),
    )
    avatar = forms.ImageField(label=_("Avatar"), required=False)

    class Meta:
        model = MyUser
        fields = ("email", "trigram", "avatar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"

        # Récupérer l'instance du profil utilisateur
        profile = self.instance._profile if hasattr(self.instance, "_profile") else None
        avatar_url = (
            profile.get_avatar_url() if profile else "/static/images/default_avatar.png"
        )

        # Ajouter un élément HTML pour afficher l'avatar actuel
        avatar_display = HTML(
            f"""
        <div class="flex justify-center mb-4">
            <img src="{avatar_url}" alt="Avatar" class="w-24 h-24 rounded-full">
        </div>
        """
        )

        self.helper.layout = Layout(
            "email",
            "trigram",
            avatar_display,
            "avatar",
            Submit(
                "submit",
                "Valider",
                css_class="button-valider",
            ),
        )
        # # Récupérer l'instance du profil utilisateur
        # if self.instance and hasattr(self.instance, '_profile'):
        #     profile = self.instance._profile
        #     self.initial['avatar'] = profile.avatar

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CQUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile, created = MemberProfile.objects.get_or_create(user=user)
            if "avatar" in self.cleaned_data and self.cleaned_data["avatar"]:
                profile.avatar = self.cleaned_data["avatar"]
                profile.save()
        return user


class PasswordResetForm(DjangoPasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].label = _("Email")
        self.fields["email"].widget = forms.EmailInput(
            attrs={
                "placeholder": _("Votre adresse email"),
                "class": "form-input",
                "autofocus": True,
            }
        )

        self.helper = FormHelper()
        self.helper.form_class = "border p-8"
        self.helper.layout = Layout(
            "email",
            Submit(
                "submit",
                "Réinitialiser le mot de passe",
                css_class="button-valider",
            ),
        )
