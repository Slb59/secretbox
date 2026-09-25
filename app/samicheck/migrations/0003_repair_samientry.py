from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("samicheck", "0002_samientry"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TABLE IF NOT EXISTS `samicheck_samientry` (
                `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
                `note` longtext NOT NULL,
                `value` integer UNSIGNED NULL CHECK (`value` >= 0),
                `day_id` bigint NOT NULL,
                `indicator_id` bigint NOT NULL,
                CONSTRAINT `unique_sami_entry_per_day_indicator`
                    UNIQUE (`day_id`, `indicator_id`),
                CONSTRAINT `samicheck_samientry_day_id_87fbf655_fk_samicheck_samiday_id`
                    FOREIGN KEY (`day_id`) REFERENCES `samicheck_samiday` (`id`),
                CONSTRAINT `samicheck_samientry_indicator_fk`
                    FOREIGN KEY (`indicator_id`) 
                        REFERENCES `samicheck_samiindicator` (`id`)
            )
        """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
