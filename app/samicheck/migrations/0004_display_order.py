from django.db import migrations, models


def initialize_display_order(apps, schema_editor):
    SamiCategory = apps.get_model("samicheck", "SamiCategory")
    SamiIndicator = apps.get_model("samicheck", "SamiIndicator")
    database = schema_editor.connection.alias

    for category_order, category in enumerate(
        SamiCategory.objects.using(database).order_by("name").iterator()
    ):
        SamiCategory.objects.using(database).filter(pk=category.pk).update(
            display_order=category_order
        )

    for category in SamiCategory.objects.using(database).all().iterator():
        for indicator_order, indicator in enumerate(
            SamiIndicator.objects.using(database)
            .filter(category_id=category.pk)
            .order_by("title")
            .iterator()
        ):
            SamiIndicator.objects.using(database).filter(pk=indicator.pk).update(
                display_order=indicator_order
            )


class Migration(migrations.Migration):
    dependencies = [("samicheck", "0003_repair_samientry")]

    operations = [
        migrations.AddField(
            model_name="samicategory",
            name="display_order",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Ordre d'affichage"
            ),
        ),
        migrations.AddField(
            model_name="samiindicator",
            name="display_order",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Ordre d'affichage"
            ),
        ),
        migrations.RunPython(initialize_display_order, migrations.RunPython.noop),
        migrations.AlterModelOptions(
            name="samicategory",
            options={
                "ordering": ["display_order", "name"],
                "verbose_name": "Catégorie Sami",
                "verbose_name_plural": "Catégories Sami",
            },
        ),
        migrations.AlterModelOptions(
            name="samiindicator",
            options={
                "ordering": [
                    "category__display_order",
                    "category__name",
                    "display_order",
                    "title",
                ],
                "verbose_name": "Indicateur",
                "verbose_name_plural": "Indicateurs",
            },
        ),
        migrations.AlterModelOptions(
            name="samientry",
            options={
                "ordering": [
                    "-day",
                    "indicator__category__display_order",
                    "indicator__category__name",
                    "indicator__display_order",
                    "indicator__title",
                ],
                "verbose_name": "Relevé",
                "verbose_name_plural": "Relevés",
            },
        ),
    ]
