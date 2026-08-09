from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class DictavoixTheme(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Thème Dictavoix"
        verbose_name_plural = "Thèmes Dictavoix"

    def __str__(self):
        return self.name


class DictavoixDictionaryWord(models.Model):
    theme = models.ForeignKey(
        DictavoixTheme,
        on_delete=models.PROTECT,
        related_name="dictionary_words",
    )
    word = models.CharField(max_length=120)
    pronunciation_hint = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Mot dictionnaire"
        verbose_name_plural = "Mots dictionnaire"
        unique_together = ("theme", "word")

    def __str__(self):
        return self.word


class DictavoixExercise(models.Model):
    theme = models.ForeignKey(
        DictavoixTheme,
        on_delete=models.PROTECT,
        related_name="exercises",
    )
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="dictavoix_exercises",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Exercice Dictavoix"
        verbose_name_plural = "Exercices Dictavoix"

    def __str__(self):
        return self.title


class DictavoixSession(models.Model):
    exercise = models.ForeignKey(
        DictavoixExercise,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="dictavoix_sessions",
    )
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    error_count = models.PositiveIntegerField(default=0)
    total_word_count = models.PositiveIntegerField(default=0)
    dictionary_word_count = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Session Dictavoix"
        verbose_name_plural = "Sessions Dictavoix"

    def __str__(self):
        return f"{self.user} - {self.exercise} ({self.started_at:%Y-%m-%d %H:%M})"
