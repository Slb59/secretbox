import logging

from django.core.exceptions import PermissionDenied


class GroupRequiredMixin:
    group_name = None  # à définir dans la vue héritée

    def dispatch(self, request, *args, **kwargs):
        print("========== GroupRequiredMixin ==========")
        print(self.group_name)
        print(request.user.groups.filter(name=self.group_name).exists())
        if request.user.is_superuser or (
            self.group_name
            and request.user.groups.filter(name=self.group_name).exists()
        ):
            return super().dispatch(request, *args, **kwargs)
        logger = logging.getLogger(__name__)
        logger.warning(f"Accès refusé pour {request.user} à {request.path}")
        raise PermissionDenied
