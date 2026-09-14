from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import Category, State

User = get_user_model()


class DevappsApplication(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"

    def __str__(self):
        return self.name


class DevappsVersion(models.Model):
    name = models.CharField(max_length=120, unique=True)
    objectif = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Version"
        verbose_name_plural = "Versions"

    def __str__(self):
        return self.name


class DevappsAction(models.Model):
    application = models.ForeignKey(
        DevappsApplication,
        on_delete=models.PROTECT,
        related_name="actions",
    )
    version = models.ForeignKey(
        DevappsVersion,
        on_delete=models.PROTECT,
        related_name="actions",
        blank=True,
        null=True,
    )
    category = models.CharField(
        max_length=20, choices=Category.choices, default=Category.ANALYSIS
    )
    description = models.TextField()
    details = models.TextField(blank=True)
    # 1  → très urgent 10 → important 50 → normal 100 → faible
    priority = models.PositiveIntegerField(default=100)
    state = models.CharField(max_length=20, choices=State.choices, default=State.TODO)
    estimated_time = models.PositiveIntegerField(help_text=_("Temps estimé en minutes"))
    achieved_time = models.PositiveIntegerField(
        blank=True, null=True, help_text=_("Temps réalisé en minutes")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    planned = models.BooleanField(default=False)
