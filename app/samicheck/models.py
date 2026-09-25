from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.utils.translation import gettext_lazy as _


class SamiCategory(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )

    max_score = models.PositiveIntegerField(
        default=25,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Catégorie Sami")
        verbose_name_plural = _("Catégories Sami")

    def __str__(self):
        return self.name


class SamiIndicator(models.Model):
    category = models.ForeignKey(
        SamiCategory,
        on_delete=models.PROTECT,
        related_name="indicators",
    )

    title = models.CharField(
        max_length=100,
        verbose_name=_("Titre"),
    )

    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Règle permettant de déterminer le niveau obtenu."),
    )

    max_level = models.PositiveIntegerField(
        default=5,
        verbose_name=_("Niveau maximum"),
    )

    class Meta:
        ordering = ["category", "title"]
        verbose_name = _("Indicateur")
        verbose_name_plural = _("Indicateurs")

    def __str__(self):
        return f"{self.category} - {self.title}"


class SamiDay(models.Model):
    date = models.DateField(
        unique=True,
        verbose_name=_("Date"),
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Début"),
    )

    ended_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Fin"),
    )

    class Meta:
        ordering: list[str] = ["-date"]
        verbose_name = _("Journée Sami")
        verbose_name_plural = _("Journées Sami")

    def __str__(self):
        return str(self.date)


class SamiEntry(models.Model):
    day = models.ForeignKey(
        SamiDay,
        on_delete=models.CASCADE,
        related_name="entries",
        verbose_name=_("Journée"),
    )

    indicator = models.ForeignKey(
        SamiIndicator,
        on_delete=models.PROTECT,
        related_name="entries",
        verbose_name=_("Indicateur"),
    )

    note = models.TextField(
        blank=True,
        verbose_name=_("Remarque"),
    )

    value = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Valeur"),
    )

    class Meta:
        ordering: list[str] = ["-day", "indicator__category", "indicator"]
        verbose_name = _("Relevé")
        verbose_name_plural = _("Relevés")
        constraints: list[UniqueConstraint] = [
            models.UniqueConstraint(
                fields=["day", "indicator"],
                name="unique_sami_entry_per_day_indicator",
            ),
        ]

    def __str__(self):
        return f"{self.day} - {self.indicator}"
