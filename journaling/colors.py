from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import CATEGORY_CHOICES, PERIODIC_CHOICES, PLACE_CHOICES, PRIORITY_CHOICES

HEX_COLOR_VALIDATOR = RegexValidator(
    regex=r"^#[0-9A-Fa-f]{6}$",
    message=_("Entrez une couleur au format hexadécimal valide (ex: #1A2B3C)."),
)


class ColorParameter(models.Model):
    """
    Model representing a color parameter for a task.
    """

    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    periodic = models.CharField(
        max_length=20, choices=[("*-Every", "tous les cas")] + PERIODIC_CHOICES
    )
    category = models.CharField(
        max_length=20, choices=[("*-Every", "tous les cas")] + CATEGORY_CHOICES
    )
    place = models.CharField(
        max_length=20, choices=[("*-Every", "tous les cas")] + PLACE_CHOICES
    )
    color = models.CharField(max_length=7, validators=[HEX_COLOR_VALIDATOR])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["priority", "periodic", "category", "place"],
                name="unique_color_combination",
            )
        ]

    def __str__(self):
        return f"{self.priority} / {self.periodic} / {self.category} / {self.place} → {self.color}"

    def get_color_parameter_coverage():
        nb_total = (
            len(PRIORITY_CHOICES)
            * len(PERIODIC_CHOICES)
            * len(CATEGORY_CHOICES)
            * len(PLACE_CHOICES)
        )
        nb_elements = ColorParameter.objects.count()
        return f"{nb_elements} / {nb_total} combinaisons définies ({round(100 * nb_elements / nb_total, 2)}%)"
