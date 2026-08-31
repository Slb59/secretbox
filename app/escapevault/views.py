"""Views for the escapevault application.
Dashboard, edit, create, delete, and list views.
"""

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)
from folium import CustomIcon, Map, Marker, Popup

from app.account.mixins import GroupRequiredMixin

from .filters import EscapeVaultFilterForm
from .forms import EscapeVaultForm
from .models import NomadePosition


class EscapeVaultBaseView(LoginRequiredMixin, GroupRequiredMixin):
    group_name = "escapevault_access"


class EscapeVaultMapView(EscapeVaultBaseView, TemplateView):
    template_name = "escapevault/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = EscapeVaultFilterForm(self.request.GET or None)

        # Create a base map centered around a specific location
        the_map = Map(location=[45.4769, 9.1516], zoom_start=5)  # Centered on France

        # Fetch all nomadic positions from the database
        positions = NomadePosition.objects.filter()

        if form.is_valid():
            data = form.cleaned_data
            if data["category"]:
                positions = positions.filter(category=data["category"])

        print(positions)

        # Add markers for each position
        for position in positions:
            icon = CustomIcon(
                icon_image=position.get_category_image(),
                icon_size=(50, 50),
                icon_anchor=(0, 0),
            )

            if position.latitude and position.longitude:
                edit_url = reverse(
                    "escapevault:edit_position", kwargs={"pk": position.pk}
                )
                edit_url += f"?next={self.request.get_full_path()}"
                popup_html = f"""
                <div>
                    <a href="{edit_url}" target="_blank" rel="noopener noreferrer">
                        Modifier
                    </a>
                </div>"""

                if position.opening_date or position.closing_date:
                    tooltip_label = f"{position.name} "
                    tooltip_label += (
                        f"({position.opening_date} - {position.closing_date})"
                    )

                else:
                    tooltip_label = position.name

                Marker(
                    location=[position.latitude, position.longitude],
                    popup=Popup(popup_html, max_width=250),
                    tooltip=tooltip_label,
                    icon=icon,
                ).add_to(the_map)

        # Convert the map to HTML
        # Folium has no public method to convert the map to HTML
        # pylint: disable=protected-access
        the_map = the_map._repr_html_()

        context["title"] = _("EscapeVault Map")
        context["logo_url"] = "/static/images/logo_ev.png"
        context["form"] = form
        context["map"] = the_map
        return context


class EscapeVaultParametersView(EscapeVaultBaseView, TemplateView):
    template_name = "escapevault/parameters.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("EscapeVault Paramètres")
        context["logo_url"] = "/static/images/logo_ev.png"
        return context


class EscapeVaultCreateView(EscapeVaultBaseView, CreateView):
    model = NomadePosition
    form_class = EscapeVaultForm
    template_name = "generic/add_template.html"
    success_url = reverse_lazy("escapevault:list_positions")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("EscapeVault nouvelle Position")
        context["logo_url"] = "/static/images/logo_ev.png"
        return context


class EscapeVaultListView(EscapeVaultBaseView, ListView):
    model = NomadePosition
    template_name = "escapevault/list_position.html"
    context_object_name = "positions"

    def get_queryset(self):
        return NomadePosition.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = EscapeVaultFilterForm(self.request.GET or None)
        positions = NomadePosition.objects.filter()

        if form.is_valid():
            data = form.cleaned_data
            if data["category"]:
                positions = positions.filter(category=data["category"])

        context["title"] = _("EscapeVault Liste")
        context["logo_url"] = "/static/images/logo_ev.png"
        context["positions"] = positions.order_by("category", "country", "city", "name")
        context["form"] = form
        return context


class EscapeVaultEditView(EscapeVaultBaseView, UpdateView):
    model = NomadePosition
    form_class = EscapeVaultForm
    template_name = "escapevault/edit_position.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        next_url = self.request.GET.get("next")
        if next_url:
            form.fields["next"] = forms.CharField(
                widget=forms.HiddenInput(), initial=next_url, required=False
            )
        return form

    def get_success_url(self):
        next_url = self.request.GET.get("next") or self.request.POST.get("next")
        if next_url:
            return next_url
        return reverse("escapevault:list_positions")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _(f"{self.object.name}")
        context["logo_url"] = "/static/images/logo_ev.png"
        return context

    def form_valid(self, form):
        new_review_text = form.cleaned_data.get("new_review", "").strip()

        if new_review_text:
            position = form.instance
            existing_reviews = position.reviews or []

            existing_reviews.append(
                {"text": new_review_text, "date": now().isoformat()}
            )

            position.reviews = existing_reviews

        return super().form_valid(form)


class EscapeVaultDeleteView(EscapeVaultBaseView, DeleteView):
    model = NomadePosition
    template_name = "escapevault/delete_position.html"
    success_url = reverse_lazy("escapevault:list_positions")
