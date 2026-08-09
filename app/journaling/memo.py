# secretbox.journaling.memo.py
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .choices import (
    ACTION_CHOICES,
    CATEGORY_CHOICES,
    PERIODIC_CHOICES,
    PLACE_CHOICES,
    PRIORITY_CHOICES,
)
from .colors import ColorParameter

User = get_user_model()

HEX_COLOR_VALIDATOR = RegexValidator(
    regex=r"^#[0-9A-Fa-f]{6}$",
    message="Entrez une couleur au format hexadécimal valide (ex: #1A2B3C).",
)


class Memo(models.Model):
    """
    Model representing a task to be accomplished in the system.

    This model allows you to manage tasks
    with their status, priority, category and assignment.
    It also includes the ability to schedule recurring tasks
    and associate them with a specific user.

    Attributs:
        state (CharField): État de la tâche avec les choix suivants :
            - todo: À faire
            - in_progress: En cours
            - done: Terminé
            - report: Reporté
        priority (CharField): Niveau de priorité de la tâche :
            - 6-verylow: Très faible
            - 5-low: Faible
            - 4-normal: Normale
            - 3-medium: Moyenne
            - 2-high: Élevée
            - 1-highest: Très élevée
        category (CharField): Catégorie de la tâche
        who (CharField): Personne responsable avec les choix suivants :
            - SLB: Sylvie
            - JCB: Jean-Christophe
            - LAU: Laurine
            - THO: Thomas
            - ODI: Odile
            - MAM: Maman
            - PAP: Papa
        place (CharField): Lieu où la tâche doit être effectuée :
            - cantin: Cantin
            - chm: CHM
            - genese: Genèse
            - partout: Partout
        periodic (CharField): Fréquence de répétition
        duration (DurationField): Durée estimée pour accomplir la tâche
        description (TextField): Description détaillée de la tâche
        appointment (DateTimeField): Date et heure prévue pour la tâche
        date (DateField): Date de création de la tâche
        done (DateField): Date de réalisation de la tâche
        note (TextField): Notes supplémentaires (optionnel)

    Méthodes:
        __str__(): Returns the task description as a string representation.
    """

    STATE_CHOICES = [
        ("todo", _("A faire")),
        ("in_progress", _("En cours")),
        ("done", _("Terminé")),
        ("report", _("Reporté")),
        ("cancel", _("Annulé")),
    ]

    APPOINTEMENT_CHOICES = [
        ("rdv", "Rendez-vous"),
        ("birthday", "Anniversaire"),
        ("festival", "Fête"),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_memos"
    )
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default="memo")
    duration = models.IntegerField(
        default=30, validators=[MinValueValidator(10), MaxValueValidator(800)]
    )
    description = models.TextField()
    appointment = models.CharField(
        max_length=20, choices=APPOINTEMENT_CHOICES, blank=True, null=True
    )
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="01-organisation"
    )
    who = models.ManyToManyField(User, related_name="assigned_memos", blank=True)
    place = models.CharField(max_length=20, choices=PLACE_CHOICES, default="partout")
    periodic = models.CharField(
        max_length=20, choices=PERIODIC_CHOICES, default="partout"
    )
    report_date = models.DateField(blank=True, null=True)
    planned_date = models.DateField(default=(date.today() + timedelta(days=1)))
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default="4-normal"
    )
    done_date = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_planned_date = self.planned_date

    @property
    def original_planned_date(self):
        return self.__original_planned_date

    def __str__(self):
        return self.description

    def check_if_state_is_cancel_or_done(self):
        if self.state == "done":
            return False, _("Cette tâche est déjà terminée")
        if self.state == "cancel":
            return False, _("Cette tâche est déjà annulée")
        return True, ""

    def next_date(self, date_of_start):
        """
        Calculate the next date based on the periodicity choice.

        Returns:
            date: The next date calculated according to the periodicity
        """
        PERIODIC_DAYS_MAPPING = {
            "01-none": 0,
            "02-everyday": 1,
            "03-every2days": 2,
            "04-every3days": 3,
            "05-every4days": 4,
            "06-every5days": 5,
            "07-everyweek": 7,
            "08-every10days": 10,
            "09-every2weeks": 14,
            "10-everymonth": 30,
            "11-every6weeks": 42,
            "12-every2months": 60,
            "13-every3months": 90,
            "14-every4months": 120,
            "15-every6months": 180,
            "16-everyyear": 365,
        }

        if not date_of_start:
            date_of_start = date.today()

        days_to_add = PERIODIC_DAYS_MAPPING[self.periodic]
        # print(f"next date: {days_to_add}")
        return date_of_start + timedelta(days=days_to_add)

    def report_element(self, date_of_report):
        """
        Reports the element to the user at today+1.

        This method sets the element's state to "report"
        and updates the date to the next date.
        """
        if not date_of_report:
            date_of_report = date.today()
        if self.state != "done":
            self.planned_date = date_of_report + timedelta(days=1)
            self.state = "report"
            if self.report_date is None:
                self.report_date = date_of_report
            self.save()

    def delete_element(self, date_of_delete):
        if not date_of_delete:
            date_of_delete = date.today()
        if self.state != "cancel":
            self.state = "cancel"
            self.note = f"*** supprimé {date_of_delete} ***\n{self.note}"
            self.save()

    def undelete_element(self, date_of_undelete):
        if not date_of_undelete:
            date_of_undelete = date.today()
        if self.state == "cancel":
            self.state = "todo"
            self.note = f"*** restauré {date_of_undelete} ***\n{self.note}"
            self.save()

    def report_element_if_not_done(self, date_of_report):
        if not date_of_report:
            date_of_report = date.today()
        if self.state != "done" and self.planned_date < date_of_report:
            self.report_element(date_of_report)

    def new_day(self, new_planned_date):
        """
        Updates the element's current date to now.
        Updates all planned dates to now.
        set the state to "report" if the element is not done.

        This method updates the element's current date to
        the next day and saves the changes.

        """
        if not new_planned_date:
            new_planned_date = date.today()

        if self.state != "done" and self.planned_date < new_planned_date:
            self.planned_date = new_planned_date
            self.state = "report"
            if self.report_date is None:
                self.report_date = new_planned_date
            self.save()

    def set_done(self, date_of_done):
        """
        Sets the element's state to "done" and updates the date done_date.
        """
        if not date_of_done:
            date_of_done = date.today()
        if self.state != "cancel":
            self.state = "done"
            self.done_date = date_of_done
            self.save()
            return True
        return False

    def get_planned_date_display(self):
        """
        Returns the formatted planned_date or an empty string if None.
        Returns:
            str: The formatted planned_date or an empty string.
        """
        return self.planned_date.strftime("%d/%m/%Y") if self.planned_date else ""

    def get_done_date_display(self):
        """
        Returns the formatted done_date or an empty string if None.
        Returns:
            str: The formatted done_date or an empty string.
        """
        return self.done_date.strftime("%d/%m/%Y") if self.done_date else ""

    def get_report_date_display(self):
        """
        Returns the formatted report_date or an empty string if None.
        Returns:
            str: The formatted report_date or an empty string.
        """
        return self.report_date.strftime("%d/%m/%Y") if self.report_date else ""

    def get_state_label(self):
        base_label = super().get_state_display()
        if self.state == "report" and self.report_date:
            return f"{base_label} le {self.get_report_date_display()}"
        return base_label

    @property
    def get_color(self) -> str:
        filters = [
            Q(
                priority=self.priority,
                periodic=self.periodic,
                category=self.category,
                place=self.place,
            ),
            Q(
                priority=self.priority,
                periodic=self.periodic,
                category=self.category,
                place="*-Every",
            ),
            Q(
                priority=self.priority,
                periodic=self.periodic,
                category="*-Every",
                place="*-Every",
            ),
            Q(
                priority=self.priority,
                periodic="*-Every",
                category="*-Every",
                place="*-Every",
            ),
        ]

        for f in filters:
            color_param = ColorParameter.objects.filter(f).first()
            if color_param:
                return color_param.color

        return "#f3faf0"  # Couleur par défaut

    def can_view(self, user):
        return (
            user.is_superuser
            or self.user == user
            or self.who.filter(pk=user.pk).exists()
        )

    def can_edit(self, user):
        return (user.is_superuser or self.user == user) and (
            self.state == "done" or self.state == "report" or self.state == "todo"
        )

    def can_edit_limited(self, user):
        return (
            self.who.filter(pk=user.pk).exists()
            and self.user != user
            and not user.is_superuser
        )

    def can_delete(self, user):
        return (user.is_superuser or self.user == user) and (
            self.state == "done"
            or self.state == "in_progress"
            or self.state == "report"
            or self.state == "todo"
        )

    def can_edit_any(self, user):
        return self.can_edit(user) or self.can_edit_limited(user)

    def can_undelete(self, user):
        return (user.is_superuser or self.user == user) and (self.state == "cancel")


class MemoHistory(models.Model):
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE, related_name="history")
    changed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="memo_changes",
    )
    timestamp = models.DateTimeField(default=timezone.now)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    changes = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        ts = timezone.localtime(self.timestamp)
        return f"{self.memo} - {self.get_action_display()} ({ts:%Y-%m-%d %H:%M:%S%z})"
