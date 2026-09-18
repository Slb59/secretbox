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
    EVENT_CHOICES,
    PERIODIC_CHOICES,
    PERIODIC_DAYS_MAPPING,
    PLACE_CHOICES,
    PRIORITY_CHOICES,
    LocationType,
    State,
)
from .colors import ColorParameter
from .services import tomorrow

User = get_user_model()

HEX_COLOR_VALIDATOR = RegexValidator(
    regex=r"^#[0-9A-Fa-f]{6}$",
    message="Entrez une couleur au format hexadécimal valide (ex: #1A2B3C).",
)


class Memo(models.Model):
    """
    Represents a task with scheduling, assignment, priority and status.

    Memos can be assigned to users, scheduled for a future date,
    repeated according to a periodicity, and marked as completed,
    reported or cancelled.

    Méthodes:
        __str__(): Returns the task description as a string representation.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_memos"
    )
    state = models.CharField(max_length=20, choices=State.choices, default=State.TODO)
    duration = models.IntegerField(
        default=30, validators=[MinValueValidator(10), MaxValueValidator(800)]
    )
    description = models.TextField()
    event_type = models.CharField(
        max_length=20, choices=EVENT_CHOICES, blank=True, null=True
    )
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="01-organisation"
    )
    who = models.ManyToManyField(User, related_name="assigned_memos", blank=True)
    place = models.CharField(max_length=20, choices=PLACE_CHOICES, default="partout")
    location_type = models.CharField(
        max_length=10,
        choices=LocationType.choices,
        default=LocationType.INDOOR,
    )
    periodic = models.CharField(
        max_length=20, choices=PERIODIC_CHOICES, default="partout"
    )
    report_date = models.DateField(blank=True, null=True)
    planned_date = models.DateField(default=tomorrow)
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default="4-normal"
    )
    # Indicates whether this memo should be processed today (checkbox in UI)
    process_today = models.BooleanField(default=False)
    done_date = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Keep the original value to detect planned_date changes.
        self.__original_planned_date = self.planned_date

    @property
    def original_planned_date(self):
        return self.__original_planned_date

    def __str__(self):
        return self.description

    def check_if_state_is_cancel_or_done(self):
        if self.state == State.DONE:
            return False, _("Cette tâche est déjà terminée")
        if self.state == State.CANCEL:
            return False, _("Cette tâche est déjà annulée")
        return True, ""

    def next_date(self, date_of_start):
        """
        Calcul la date suivante basée sur le choix de périodicité.
        Il y a un problème sur le calcul du mois suivant,
        ici c'est +30 jours, mais il faudrait calculer le mois suivant exact.

        Returns:
            date: The next date calculated according to the periodicity
        """

        if not date_of_start:
            date_of_start = date.today()

        days_to_add = PERIODIC_DAYS_MAPPING[self.periodic]

        return date_of_start + timedelta(days=days_to_add)

    def report(self, date_of_report):
        """
        Reports the element to the user at today+1.

        This method sets the element's state to "report"
        and updates the date to the next date.
        """
        if date_of_report is None:
            date_of_report = date.today()
        if self.state != State.DONE:
            self.planned_date = date_of_report + timedelta(days=1)
            self.state = State.REPORT
            if self.report_date is None:
                self.report_date = date_of_report
            self.save()

    def cancel(self, date_of_delete):
        if date_of_delete is None:
            date_of_delete = date.today()
        if self.state != State.CANCEL:
            self.state = State.CANCEL
            self.note = f"*** annulé le {date_of_delete} ***\n{self.note}"
            self.save()

    def restore(self, date_of_undelete):
        if not date_of_undelete:
            date_of_undelete = date.today()
        if self.state == State.CANCEL:
            self.state = State.TODO
            self.note = f"*** restauré le {date_of_undelete} ***\n{self.note}"
            self.save()

    def report_if_not_done(self, date_of_report):
        if not date_of_report:
            date_of_report = date.today()
        if self.state != State.DONE and self.planned_date < date_of_report:
            self.report(date_of_report)

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

        if self.state != State.DONE and self.planned_date < new_planned_date:
            self.planned_date = new_planned_date
            self.state = State.REPORT
            if self.report_date is None:
                self.report_date = new_planned_date
            self.save()

    def mark_as_done(self, date_of_done):
        """
        Sets the element's state to "done" and updates the date done_date.
        """
        if not date_of_done:
            date_of_done = date.today()
        if self.state != State.CANCEL:
            self.state = State.DONE
            self.done_date = date_of_done
            self.save()
            return True
        return False

    def _format_date(self, value):
        return value.strftime("%d/%m/%Y") if value else ""

    def get_planned_date_display(self):
        """
        Returns the formatted planned_date or an empty string if None.
        Returns:
            str: The formatted planned_date or an empty string.
        """
        return self._format_date(self.planned_date)

    def get_done_date_display(self):
        """
        Returns the formatted done_date or an empty string if None.
        Returns:
            str: The formatted done_date or an empty string.
        """
        return self._format_date(self.done_date)

    def get_report_date_display(self):
        """
        Returns the formatted report_date or an empty string if None.
        Returns:
            str: The formatted report_date or an empty string.
        """
        return self._format_date(self.report_date)

    def get_state_label(self):
        base_label = super().get_state_display()
        if self.state == State.REPORT and self.report_date:
            return f"{base_label} le {self.get_report_date_display()}"
        return base_label

    def _find_color_parameter(self):
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

        for condition in filters:
            color_parameter = ColorParameter.objects.filter(condition).first()
            if color_parameter:
                return color_parameter

        return None

    @property
    def get_color(self) -> str:
        color_parameter = self._find_color_parameter()
        return color_parameter.color if color_parameter else "#f3faf0"

    def can_view(self, user):
        return (
            user.is_superuser
            or self.user == user
            or self.who.filter(pk=user.pk).exists()
        )

    def can_edit(self, user):
        editable_states = {State.TODO, State.REPORT, State.DONE}
        return (
            user.is_superuser or self.user == user
        ) and self.state in editable_states

    def can_edit_limited(self, user):
        return (
            self.who.filter(pk=user.pk).exists()
            and self.user != user
            and not user.is_superuser
        )

    def can_delete(self, user):
        deletable_states = {State.TODO, State.IN_PROGRESS, State.REPORT, State.DONE}
        return (
            user.is_superuser or self.user == user
        ) and self.state in deletable_states

    def can_edit_any(self, user):
        return self.can_edit(user) or self.can_edit_limited(user)

    def can_undelete(self, user):
        return (user.is_superuser or self.user == user) and (self.state == State.CANCEL)


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
