import locale

from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def format_title(value):
    if isinstance(value, timezone.datetime):
        # Définir la locale à français
        locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
        # Formatez la date selon vos besoins
        return value.strftime("%A %d %B %Y")
    return value


@register.filter
def can_edit_any(memo, user):
    return memo.can_edit_any(user)


@register.filter
def can_delete(memo, user):
    return memo.can_delete(user)


@register.filter
def can_edit(memo, user):
    return memo.can_edit(user)


@register.filter
def can_edit_limited(memo, user):
    return memo.can_edit_limited(user)


@register.filter
def can_undelete(memo, user):
    return memo.can_undelete(user)


@register.filter
def is_not_done(memo):
    return memo.state != "done"


@register.filter
def is_stopwtach_inactive(user):
    return not user.stopwatch
