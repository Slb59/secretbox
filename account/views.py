#account/views.py

from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView as DjangoLoginView,
    LogoutView as DjangoLogoutView,
    PasswordResetView as DjangoPasswordResetView,
)
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from .forms import LoginForm, PasswordResetForm, ProfileUpdateForm

MYUSER = get_user_model()


def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

class MyLoginView(DjangoLoginView):

    form_class = LoginForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("home")

    def get_success_url(self):
        url = self.success_url
        print(url)
        return url

    def form_valid(self, form):
        print("\n=== Authentification ===")
        login(self.request, form.get_user())
        response = super().form_valid(form)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Connexion")
        context["logo_url"] = "/static/images/secretbox/logo_sb.png"
        return context

    def form_invalid(self, form):
        # print("=== Formulaire invalide ===")
        # print(form.errors)
        return super().form_invalid(form)


class MyLogoutView(DjangoLogoutView):
    template_name = "registration/logout.html"
    success_url = reverse_lazy("login")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = MYUSER
    form_class = ProfileUpdateForm
    template_name = "secretbox/profile.html"
    success_url = reverse_lazy("dashboard")

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["title"] = _("Vos données")
        context["logo_url"] = "/static/images/logo_sb.png"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("Your profile has been updated successfully."))
        return response

    def form_invalid(self, form):
        messages.error(self.request, _("Please correct the errors below."))
        return super().form_invalid(form)


class PasswordResetView(DjangoPasswordResetView):
    form_class = PasswordResetForm
    template_name = "registration/password_reset.html"
    email_template_name = "registration/password_reset_email.html"
    success_url = reverse_lazy("users:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Reinitialisation du mot de passe")
        context["logo_url"] = "/static/images/logo_sb.png"
        return context

    def form_valid(self, form):
        print("\n=== DEBUG EMAIL ===")
        print(f"Email cible: {form.cleaned_data['email']}")
        return super().form_valid(form)
