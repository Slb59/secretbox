from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, View
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .memo import Memo
from .forms import MemoForm

class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'journaling/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": _("Bienvenue dans SecretBox"),
                "logo_url": "/theme/static/images/secret.jpeg",
                "request": self.request,
            }
        )
        return context

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        context = {}
        return self.render_to_response(context)

class MemoCreateView(LoginRequiredMixin, CreateView):
    model = Memo
    form_class = MemoForm
    template_name = "journaling/add_template.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Nouvelle entrée")
        context["logo_url"] = "/static/images/secretbox/logo_sb2.png"
        return context

    def form_valid(self, form):
        todo = form.save(commit=False)
        todo.user = self.request.user
        todo.save()

        # Afficher les assignés
        todo.who.add(self.request.user)
        assignees = todo.who.all()
        print(f"Assignés: {[user.trigram for user in assignees]}")
        todo.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning(f"Form invalid:{self.__class__.__name__} {form.errors}")
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

class MemoUpdateView(LoginRequiredMixin, UpdateView):
    model = Memo
    form_class = MemoForm
    template_name = "journaling/add_template.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Modifier l'entrée")
        context["logo_url"] = "/static/images/secretbox/logo_sb2.png"
        return context

    def dispatch(self, request, *args, **kwargs):
        memo = self.get_object()
        if not memo.can_view(request.user):
            return HttpResponseForbidden(_("Vous ne pouvez pas voir cet élément."))

        if not (memo.can_edit(request.user) or memo.can_edit_limited(request.user)):
            return HttpResponseForbidden(_("Vous ne pouvez pas modifier cet élément."))

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # pour le formulaire
        return kwargs


class MemoDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        memo = get_object_or_404(Memo, pk=pk)
        if memo.state != "cancel":
            memo.state = "cancel"
            memo.note = f"*** supprimé {date.today()} ***\n{memo.note}"
            memo.save()
        return redirect("home")

    def dispatch(self, request, *args, **kwargs):
        memo = self.get_object()
        if not memo.can_delete(request.user):
            return HttpResponseForbidden(_("Vous ne pouvez pas supprimer cet élément."))
        return super().dispatch(request, *args, **kwargs)

class MemoUnDeleteView(LoginRequiredMixin, View):
    model = Memo
    success_url = reverse_lazy("home")

    def post(self, request, pk, *args, **kwargs):
        memo = get_object_or_404(Memo, pk=pk)
        if not memo.can_undelete(request.user):
            messages.error(request, _("Vous ne pouvez pas restaurer cet élément."))
            return redirect("home")

        try:
            memo.undelete_element()
            messages.success(request, _("Memo restauré"))
        except Exception as e:
            messages.error(request, _("Erreur lors de la restauration : ") + str(e))

        return redirect("home")