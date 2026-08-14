# journaling.management.commands.import_memo
import csv
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from journaling.memo import Memo

User = get_user_model()


class Command(BaseCommand):
    help = "Importe des mémos à partir d'un fichier CSV"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file", type=str, help="Le chemin vers le fichier CSV à importer"
        )

    def handle(self, *args, **options):
        csv_file = options["csv_file"]
        # Dictionnaires de mappage pour les choix
        STATE_MAP = {
            "done": "done",
            "todo": "todo",
            "annulé": "cancel",
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
            "Achat-livre": "03-achat",
            "04-sport": "04-sport",
            "sport": "04-sport",
            "05-sante": "05-sante",
            "santé": "05-sante",
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
        }
        PERIODIC_MAP = {
            "None": "01-none",
            "none": "01-none",
            "04-none": "01-none",
            "01-every day": "02-everyday",
            "02-every 2 days": "03-every2days",
            "03-every 3 days": "04-every3days",
            "05-every 4 days": "05-every4days",
            "06-every 5 days": "06-every5days",
            "07-every week": "07-everyweek",
            "08-every 10 days": "08-every10days",
            "every 2 weeks": "09-every2weeks",
            "09-every 2 weeks": "09-every2weeks",
            "10-every 3 weeks": "10-every3weeks",
            "every month": "11-everymonth",
            "11-every month": "11-everymonth",
            "12-every 6 weeks": "12-every6weeks",
            "12-every 2 months": "13-every2months",
            "13-every 2 months": "13-every2months",
            "14-every 3 months": "14-every3months",
            "13-every 3 months": "14-every3months",
            "15-every 4 months": "15-every4months",
            "16-every 6 months": "16-every6months",
            "every year": "17-everyyear",
            "17-every year": "17-everyyear",
            "18-every 18 months": "18-every18months",
            "19-every 2 years": "19-every2years",
        }

        RDV_MAP = {
            "x": "rdv",
            "Rdv": "rdv",
            "anniversaire": "birthday",
        }

        PLACE_MAP = {
            "br30": "chm",
            "chm": "chm",
            "Cantin-ext": "cantin-ext",
            "cantin_int": "cantin-int",
            "genèse": "genese",
            "fontaine": "fontaine",
            "fnd": "fontaine",
            "cantin": "cantin-ext",
        }

        USER_MAP = {
            "syl": "slb",
            "sylvie": "slb",
            "laurine": "lau",
            "jcb": "jcb",
            "thomas": "tom",
            "odile": "jcb",
        }

        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Crée ou récupère l'utilisateur créateur
                    creator, _ = User.objects.get_or_create(trigram="slb")

                    # Convertit les dates (ex: 02/07/2024 → 2024-07-02)
                    planned_date = (
                        datetime.strptime(row["Date"], "%d/%m/%Y").date()
                        if row["Date"]
                        else None
                    )
                    done_date = (
                        datetime.strptime(row["Done"], "%d/%m/%Y").date()
                        if row["Done"]
                        else None
                    )

                    # Crée le memo
                    memo = Memo.objects.create(
                        user=creator,
                        state=STATE_MAP.get(row["Etat"], "todo"),
                        duration=int(row["Durée"]) if row["Durée"] else 30,
                        description=row["Description"],
                        appointment=RDV_MAP.get(row["Rdv"]) if row["Rdv"] else None,
                        category=TYPE_MAP.get(
                            row["Type"], "01-organisation"
                        ),  # Valeur par défaut
                        place=PLACE_MAP.get(row["Lieu"], "cantin-ext"),
                        periodic=PERIODIC_MAP.get(row["Périodique"]),
                        planned_date=planned_date,
                        priority=PRIORITY_MAP.get(row["Priorité"], "4-normal"),
                        done_date=done_date,
                        note=row["Note"] if row["Note"] else None,
                    )
                    user = User.objects.get(trigram=USER_MAP.get(row["Qui"], "slb"))
                    memo.who.add(user)
                    memo.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully imported memo: {memo.description}"
                        )
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error importing row: {row}. Error: {e}")
                    )
                    exit(1)
