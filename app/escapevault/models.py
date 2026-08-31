import re

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import Countries, CountryField


def validate_city_format(value):
    if len(value) > 40:
        raise ValidationError("The city name is too long.")

    if not all(c.isalpha() or c.isspace() or c == "-" for c in value):
        raise ValidationError("The city name contains invalid characters.")


def validate_day_month_format(value):
    # Utilisez une expression régulière pour valider le format DD/MM
    if not re.match(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])$", value):
        raise ValidationError("The correct format is DD/MM.")


class NomadePosition(models.Model):
    """
    Model representing a nomade position.
    This nomade is not affected to a user.
    Any connected user that has the access to the escapevault application can see,
    update or delete it.
    """

    CATEGORY_HOME = "home"
    CATEGORY_NOMADE = "nomade"
    CATEGORY_LOVE = "love"
    CATEGORY_PLAIN = "plain"
    CATEGORY_BAN = "ban"

    CATEGORY_CHOICES = [
        (CATEGORY_HOME, _("Maison")),
        (CATEGORY_NOMADE, _("Nomade")),
        (CATEGORY_LOVE, _("Coup de coeur")),
        (CATEGORY_PLAIN, _("Ordinaire")),
        (CATEGORY_BAN, _("À bannir")),
    ]

    # Core Information
    name = models.CharField(max_length=255)

    # Location Details
    address = models.TextField()
    city = models.TextField(max_length=40, validators=[validate_city_format])

    class NomadeCountries(Countries):
        only = ["CA", "FR", "DE", "IT", "JP", "RU", "GB"]

    country = CountryField(
        countries=NomadeCountries, default="FR", blank_label="(select country)"
    )

    # Rating System
    stars = models.IntegerField(
        default=0, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    reviews = models.JSONField(default=list)

    # Opening and Closing Dates
    opening_date = models.CharField(
        max_length=5, validators=[validate_day_month_format], null=True, blank=True
    )
    closing_date = models.CharField(
        max_length=5, validators=[validate_day_month_format], null=True, blank=True
    )

    # Category and Position
    category = models.CharField(
        max_length=100, choices=CATEGORY_CHOICES, default=CATEGORY_PLAIN
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
    )
    link_to_site = models.URLField(blank=True, null=True)

    def get_position(self):
        return (self.latitude, self.longitude)

    def set_position(self, lat, lon):
        self.latitude = lat
        self.longitude = lon

    def __str__(self):
        return f"{self.name} ({self.city})"

    class Meta:
        verbose_name = "Nomade Position"
        verbose_name_plural = "Nomade Positions"

    def get_category_image(self):
        if self.category:
            icon_image = f"static/icons/escapevault/{self.category}.png"
        else:
            icon_image = "static/icons/escapevault/default.png"
        return icon_image

    def get_opening_date_display(self):
        if self.opening_date:
            return self.opening_date
        return ""

    def get_closing_date_display(self):
        if self.closing_date:
            return self.closing_date
        return ""
