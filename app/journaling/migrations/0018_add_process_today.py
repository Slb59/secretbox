# Generated manually to add process_today field
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("journaling", "0017_alter_memo_planned_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="memo",
            name="process_today",
            field=models.BooleanField(default=False),
        ),
    ]
