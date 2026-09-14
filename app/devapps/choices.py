from django.db import models
from django.utils.translation import gettext_lazy as _


class State(models.TextChoices):
    TODO = "todo", _("À faire")
    CANCEL = "cancel", _("Annulé")
    IN_PROGRESS = "in_progress", _("En cours")
    DONE = "done", _("Terminé")


class Category(models.TextChoices):
    BUG = "bug", _("Bug")
    IMPROVEMENT = "improvement", _("Amélioration")
    FORMATION = "formation", _("Formation")
    CREATE = "create", _("Création")
    ANALYSIS = "analysis", _("Analyse")
    TEST = "test", _("Test")
    REFACTORING = "refactoring", _("Refactoring")
    DOCUMENTATION = "documentation", _("Documentation")
    DEPLOYMENT = "deployment", _("Déploiement")
