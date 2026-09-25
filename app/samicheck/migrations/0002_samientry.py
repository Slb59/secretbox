import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("samicheck", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SamiEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("note", models.TextField(blank=True, verbose_name="Remarque")),
                (
                    "value",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Valeur"
                    ),
                ),
                (
                    "day",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entries",
                        to="samicheck.samiday",
                        verbose_name="Journée",
                    ),
                ),
                (
                    "indicator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="entries",
                        to="samicheck.samiindicator",
                        verbose_name="Indicateur",
                    ),
                ),
            ],
            options={
                "verbose_name": "Relevé",
                "verbose_name_plural": "Relevés",
                "ordering": ["-day", "indicator__category", "indicator"],
                "constraints": [
                    models.UniqueConstraint(
                        fields=("day", "indicator"),
                        name="unique_sami_entry_per_day_indicator",
                    )
                ],
            },
        ),
    ]
