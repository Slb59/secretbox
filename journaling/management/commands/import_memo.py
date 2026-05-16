#journaling.management.commands.import_memo
import csv
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from journaling.memo import Memo

User = get_user_model()

class Command(BaseCommand):
    help = 'Importe des mémos à partir d\'un fichier CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Le chemin vers le fichier CSV à importer')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
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
            "6-verylow": "6-verylow",
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
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                