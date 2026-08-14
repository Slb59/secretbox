from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Any

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from journaling.memo import Memo

User = get_user_model()

STATE_MAP = {
    "done": "done",
    "todo": "todo",
    "annulé": "cancel",
    "annule": "cancel",
    "cancel": "cancel",
    "in_progress": "in_progress",
    "report": "report",
}

PRIORITY_MAP = {
    "1-highest": "1-highest",
    "2-high": "2-high",
    "3-medium": "3-medium",
    "4-normal": "4-normal",
    "5-low": "5-low",
    "6-lowest": "6-lowest",
}

TYPE_MAP = {
    "01-organisation": "01-organisation",
    "organisation": "01-organisation",
    "02-compta": "02-compta",
    "compta": "02-compta",
    "03-achat": "03-achat",
    "achat-livre": "03-achat",
    "04-sport": "04-sport",
    "sport": "04-sport",
    "05-sante": "05-sante",
    "santé": "05-sante",
    "05-santé": "05-sante",
    "06-contact": "06-contact",
    "contact": "06-contact",
    "07-informatique": "07-informatique",
    "informatique": "07-informatique",
    "08-menage": "08-menage",
    "menage": "08-menage",
    "09-jardin": "09-jardin",
    "jardin": "09-jardin",
    "10-doudou": "10-doudou",
    "doudou": "10-doudou",
    "11-bricoles": "11-bricoles",
    "bricoles": "11-bricoles",
    "12-couture": "12-couture",
    "couture": "12-couture",
    "13-loisirs": "13-loisirs",
    "loisirs": "13-loisirs",
    "14-vacances": "14-vacances",
    "vacances": "14-vacances",
}

PERIODIC_MAP = {
    "none": "01-none",
    "04-none": "01-none",
    "01-every day": "02-everyday",
    "02-every 2 days": "03-every2days",
    "03-every 3 days": "04-every3days",
    "05-every 4 days": "05-every4days",
    "06-every 5 days": "06-every5days",
    "07-every week": "07-everyweek",
    "08-every 10 days": "08-every10days",
    "09-every 2 weeks": "09-every2weeks",
    "10-every 3 weeks": "10-every3weeks",
    "every month": "11-everymonth",
    "11-every month": "11-everymonth",
    "12-every 6 weeks": "12-every6weeks",
    "12-every 2 months": "13-every2months",
    "13-every 2 months": "13-every2months",
    "13-every 3 months": "14-every3months",
    "14-every 3 months": "14-every3months",
    "15-every 4 months": "15-every4months",
    "16-every 6 months": "16-every6months",
    "every year": "17-everyyear",
    "17-every year": "17-everyyear",
    "18-every 18 months": "18-every18months",
    "19-every 2 years": "19-every2years",
}

RDV_MAP = {
    "x": "rdv",
    "rdv": "rdv",
    "anniversaire": "birthday",
}

PLACE_MAP = {
    "br30": "chm",
    "chm": "chm",
    "cantin-ext": "cantin-ext",
    "cantin_int": "cantin-int",
    "cantin": "cantin-ext",
    "genèse": "genese",
    "genese": "genese",
    "fontaine": "fontaine",
    "fnd": "fontaine",
}

USER_MAP = {
    "syl": "slb",
    "sylvie": "slb",
    "laurine": "lau",
    "jcb": "jcb",
    "thomas": "tom",
    "odile": "jcb",
}

DEFAULT_USER_TRIGRAM = "slb"
DEFAULT_STATE = "todo"
DEFAULT_DURATION = 30
DEFAULT_CATEGORY = "01-organisation"
DEFAULT_PLACE = "partout"
DEFAULT_PERIODIC = "01-none"
DEFAULT_PRIORITY = "4-normal"


class Command(BaseCommand):
    help = "Delete all Memo rows then import memos from a CSV file."

    def add_arguments(self, parser: Any) -> None:
        default_csv = "./media/memo.csv"
        default_reject = "./media/memo_rejects.csv"
        default_summary = "./media/memo_import_summary.txt"

        parser.add_argument(
            "--csv-file",
            type=str,
            default=str(default_csv),
            help="Path to the CSV file to import.",
        )
        parser.add_argument(
            "--reject-file",
            type=str,
            default=str(default_reject),
            help="Path to the rejected rows CSV output.",
        )
        parser.add_argument(
            "--summary-file",
            type=str,
            default=str(default_summary),
            help="Path to the summary text output.",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        csv_path = Path(options["csv_file"])
        reject_path = Path(options["reject_file"])
        summary_path = Path(options["summary_file"])

        if not csv_path.exists():
            self.stderr.write(self.style.ERROR(f"CSV file not found: {csv_path}"))
            return

        memo_count = Memo.objects.count()
        deleted_count, deleted_details = Memo.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(
                f"Deleted {memo_count} Memo rows ("
                + "total objects deleted: {deleted_count})."
            )
        )

        integrated = 0
        rejected = 0
        rejected_rows: list[dict[str, str]] = []

        with csv_path.open(newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
            for row_number, raw_row in enumerate(reader, start=2):
                row = self.clean_row(raw_row)
                try:
                    self.import_memo_row(row)
                    integrated += 1
                except Exception as exc:
                    rejected += 1
                    row["Error"] = str(exc)
                    row["Row"] = str(row_number)
                    rejected_rows.append(row)
                    self.stderr.write(
                        self.style.ERROR(f"Rejected row {row_number}: {exc}")
                    )

        if rejected_rows:
            fieldnames = list(rejected_rows[0].keys())
            with reject_path.open("w", newline="", encoding="utf-8") as reject_file:
                writer = csv.DictWriter(reject_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rejected_rows)
            self.stdout.write(
                self.style.WARNING(f"Wrote {rejected} rejected rows to {reject_path}")
            )
        else:
            self.stdout.write(self.style.SUCCESS("No rejected rows."))

        summary_lines = [
            f"CSV source: {csv_path}",
            f"Rejected file: {reject_path}",
            f"Integrated rows: {integrated}",
            f"Rejected rows: {rejected}",
        ]
        summary_text = "\n".join(summary_lines)
        summary_path.write_text(summary_text, encoding="utf-8")
        self.stdout.write(self.style.SUCCESS(summary_text))
        self.stdout.write(self.style.SUCCESS(f"Summary written to {summary_path}"))

    def normalize(self, value: str | None) -> str:
        if value is None:
            return ""
        return value.strip()

    def normalize_key(self, value: str | None) -> str:
        return self.normalize(value).lower()

    def parse_date(self, value: str | None, field_name: str) -> datetime.date | None:
        value = self.normalize(value)
        if not value:
            return None
        try:
            return datetime.strptime(value, "%d/%m/%Y").date()
        except ValueError as exc:
            raise ValueError(f"Invalid {field_name}: {value}") from exc

    def parse_int(self, value: str | None, field_name: str, default: int) -> int:
        value = self.normalize(value)
        if not value:
            return default
        try:
            return int(value)
        except ValueError as exc:
            raise ValueError(f"Invalid {field_name}: {value}") from exc

    def find_user(self, trigram: str | None):
        trigram = self.normalize_key(trigram)
        if not trigram:
            trigram = DEFAULT_USER_TRIGRAM
        trigram = USER_MAP.get(trigram, trigram)
        user, created = User.objects.get_or_create(
            trigram=trigram,
            defaults={"email": f"{trigram}@example.com"},
        )
        if created:
            user.save()
        return user

    def get_choice(
        self, mapping: dict[str, str], raw_value: str | None, default: str
    ) -> str:
        key = self.normalize_key(raw_value)
        if key == "":
            return default
        return mapping.get(key, default)

    def import_memo_row(self, row: dict[str, str]) -> Memo:
        planned_date = self.parse_date(row.get("Date"), "Date")
        done_date = self.parse_date(row.get("Done"), "Done")
        duration = self.parse_int(row.get("Durée"), "Durée", DEFAULT_DURATION)

        memo = Memo.objects.create(
            user=self.find_user(row.get("Qui")),
            state=self.get_choice(STATE_MAP, row.get("Etat"), DEFAULT_STATE),
            duration=duration,
            description=self.normalize(row.get("Description")),
            appointment=self.get_choice(RDV_MAP, row.get("Rdv"), "") or None,
            category=self.get_choice(TYPE_MAP, row.get("Type"), DEFAULT_CATEGORY),
            place=self.get_choice(PLACE_MAP, row.get("Lieu"), DEFAULT_PLACE),
            periodic=self.get_choice(
                PERIODIC_MAP, row.get("Périodique"), DEFAULT_PERIODIC
            ),
            planned_date=planned_date or datetime.today().date(),
            priority=self.get_choice(
                PRIORITY_MAP, row.get("Priorité"), DEFAULT_PRIORITY
            ),
            done_date=done_date,
            note=self.normalize(row.get("Note")) or None,
        )
        memo.save()

        who_trigram = self.normalize_key(row.get("Qui"))
        if not who_trigram:
            who_trigram = DEFAULT_USER_TRIGRAM
        who_user = self.find_user(who_trigram)
        memo.who.add(who_user)

        return memo

    def clean_row(self, raw_row: dict[str | None, str]) -> dict[str, str]:
        return {
            str(key): self.normalize(value)
            for key, value in raw_row.items()
            if key is not None
        }
