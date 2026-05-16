Pour importer des données CSV dans ta base de données Django pour le modèle `Memo`, voici une **méthode complète et adaptée** à ta structure. Je vais te guider étape par étape, en tenant compte des **champs spécifiques** de ton modèle (comme `STATE_CHOICES`, `PRIORITY_CHOICES`, etc.) et des **conversions nécessaires** (ex: dates, relations ManyToMany).

---

---

---

## **📌 Étape 1 : Préparer ton fichier CSV**
Ton fichier CSV doit être **nettoyé et structuré** pour correspondre aux champs de ton modèle `Memo`.
Voici un exemple de **mappage entre ton CSV et ton modèle** :

| **Champ CSV**       | **Champ Django (`Memo`)** | **Type/Conversion nécessaire**                     | **Exemple**          |
|---------------------|---------------------------|---------------------------------------------------|----------------------|
| Etat                | `state`                   | Mapper vers `STATE_CHOICES` (ex: `"done"` → `"done"`) | `"done"`            |
| Durée               | `duration`                | Entier (en minutes)                                | `15`                |
| Description         | `description`             | Texte brut                                         | `"Effectuer règlement arna"` |
| Rdv                 | `appointment`             | Mapper vers `APPOINTEMENT_CHOICES` (ou `None`)     | `None` ou `"rdv"`    |
| Type                | `category`                | Mapper vers `CATEGORY_CHOICES`                     | `"compta"` → `"02-comptabilite"` |
| Qui                 | `who` (ManyToManyField)   | Lier aux utilisateurs (ex: `"SLB"` → `User` Sylvie) | `"SLB"`             |
| Lieu                | `place`                   | Mapper vers `PLACE_CHOICES`                        | `"partout"`         |
| Périodique          | `periodic`                | Mapper vers `PERIODIC_CHOICES`                     | `"None"` → `None`   |
| Date                | `planned_date`            | Convertir en `YYYY-MM-DD` (ex: `02/07/2024` → `2024-07-02`) | `2024-07-02` |
| Priorité            | `priority`                | Mapper vers `PRIORITY_CHOICES` (ex: `"1-highest"`) | `"1-highest"`       |
| Done                | `done_date`               | Convertir en `YYYY-MM-DD` (ex: `01/07/2024` → `2024-07-01`) | `2024-07-01` |
| today               | (Ignorer)                 | Champ non utilisé dans ton modèle                  | -                    |
| Note                | `note`                    | Texte brut (optionnel)                             | `""`                |

---

---

## **📌 Étape 2 : Créer un script d'import CSV**
Crée un fichier `import_memos.py` dans ton projet (ex: `journaling/management/commands/import_memos.py`) pour utiliser une **commande Django personnalisée**.

### **Structure du script :**
```bash
# Crée le dossier si nécessaire
mkdir -p journaling/management/commands
touch journaling/management/commands/__init__.py
touch journaling/management/commands/import_memos.py
```

---

### **📄 Contenu de `import_memos.py` :**
```python
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from journaling.models import Memo

class Command(BaseCommand):
    help = "Import memos from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        # Dictionnaires de mappage pour les choix
        STATE_MAP = {
            "done": "done",
            "todo": "todo",
            "in_progress": "in_progress",
            "report": "report",
            "cancel": "cancel",
        }

        PRIORITY_MAP = {
            "1-highest": "1-highest",
            "2-high": "2-high",
            "3-medium": "3-medium",
            "4-normal": "4-normal",
            "5-low": "5-low",
            "6-verylow": "6-verylow",
        }

        # Exemple de mappage pour `category` (à adapter selon tes CATEGORY_CHOICES)
        CATEGORY_MAP = {
            "compta": "02-comptabilite",  # Exemple : à remplacer par tes vraies valeurs
            # Ajoute d'autres mappages ici
        }

        PLACE_MAP = {
            "cantin": "cantin",
            "chm": "chm",
            "genese": "genese",
            "partout": "partout",
        }

        PERIODIC_MAP = {
            "None": None,
            # Ajoute d'autres mappages si nécessaire
        }

        APPOINTMENT_MAP = {
            "rdv": "rdv",
            "birthday": "birthday",
            "festival": "festival",
        }

        # Mappage des utilisateurs (ex: "SLB" → User Sylvie)
        USER_MAP = {
            "SLB": "sylvie",  # Remplace par le username de Sylvie
            "JCB": "jean-christophe",
            "LAU": "laurine",
            # Ajoute d'autres utilisateurs ici
        }

        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Crée ou récupère l'utilisateur créateur (ex: Sylvie)
                    creator, _ = User.objects.get_or_create(
                        username="sylvie"  # Remplace par le créateur par défaut
                    )

                    # Convertit les dates (ex: 02/07/2024 → 2024-07-02)
                    planned_date = datetime.strptime(row['Date'], '%d/%m/%Y').date() if row['Date'] else None
                    done_date = datetime.strptime(row['Done'], '%d/%m/%Y').date() if row['Done'] else None

                    # Crée le memo
                    memo = Memo.objects.create(
                        user=creator,
                        state=STATE_MAP.get(row['Etat'], 'todo'),
                        duration=int(row['Durée']) if row['Durée'] else 30,
                        description=row['Description'],
                        appointment=APPOINTMENT_MAP.get(row['Rdv']) if row['Rdv'] else None,
                        category=CATEGORY_MAP.get(row['Type'], '01-organisation'),  # Valeur par défaut
                        place=PLACE_MAP.get(row['Lieu'], 'partout'),
                        periodic=PERIODIC_MAP.get(row['Périodique']),
                        planned_date=planned_date,
                        priority=PRIORITY_MAP.get(row['Priorité'], '4-normal'),
                        done_date=done_date,
                        note=row['Note'] if row['Note'] else None,
                    )

                    # Gère le champ ManyToMany `who` (ex: "SLB" → User Sylvie)
                    if row['Qui']:
                        users = row['Qui'].split(',')  # Si plusieurs utilisateurs sont séparés par des virgules
                        for user_key in users:
                            username = USER_MAP.get(user_key.strip())
                            if username:
                                user = User.objects.get(username=username)
                                memo.who.add(user)

                    self.stdout.write(self.style.SUCCESS(f'Successfully imported memo: {memo.description}'))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error importing row: {row}. Error: {e}'))
```

---

---

## **📌 Étape 3 : Exécuter le script d'import**
1. **Place ton fichier CSV** dans ton projet (ex: `data/memos.csv`).
2. **Exécute la commande** :
   ```bash
   uv run python manage.py import_memos data/memos.csv
   ```

---

---

## **🔍 Points clés à vérifier :**
1. **Mappage des choix** :
   - Adapte `STATE_MAP`, `PRIORITY_MAP`, `CATEGORY_MAP`, etc. **selon tes `CHOICES` réels** dans `models.py`.
   - Exemple : Si `CATEGORY_CHOICES` contient `("02-comptabilite", "Comptabilité")`, alors `CATEGORY_MAP` doit mapper `"compta"` → `"02-comptabilite"`.

2. **Utilisateurs** :
   - Assure-toi que les utilisateurs (ex: `sylvie`, `jean-christophe`) **existent** dans ta base.
   - Si tu utilises des **identifiants courts** (ex: `"SLB"`), mappe-les vers les `username` réels.

3. **Champs `ManyToMany`** :
   - Le champ `who` est un `ManyToManyField`. Dans ton CSV, si plusieurs utilisateurs sont séparés par des virgules (ex: `"SLB,JCB"`), le script les ajoutera tous.

4. **Dates** :
   - Les dates dans ton CSV sont au format `JJ/MM/AAAA`. Le script les convertit en `AAAA-MM-JJ` (format Django).

5. **Champs vides** :
   - Les champs vides dans le CSV (ex: `Rdv`, `Note`) sont gérés avec des valeurs par défaut (`None` ou `""`).

---

---

## **📌 Étape 4 : Vérifier les données importées**
Après l'import, vérifie que tout s'est bien passé :
```bash
uv run python manage.py shell
```
```python
from journaling.models import Memo
print(Memo.objects.count())  # Nombre de memos importés
print(Memo.objects.first().description)  # Affiche la description du premier memo
```

---

---

## **💡 Alternative : Utiliser `pandas` pour un import plus robuste**
Si ton CSV est complexe (beaucoup de lignes, formats variables), tu peux utiliser `pandas` pour le lire :

1. Installe `pandas` :
   ```bash
   uv add pandas
   ```

2. Modifie le script pour utiliser `pandas` :
   ```python
   import pandas as pd

   def handle(self, *args, **options):
       csv_file = options['csv_file']
       df = pd.read_csv(csv_file, encoding='utf-8')

       for _, row in df.iterrows():
           # Même logique que précédemment, mais avec row['Etat'], row['Durée'], etc.
           ...
   ```

---

---

## **⚠️ Erreurs courantes et solutions :**
| **Erreur** | **Cause** | **Solution** |
|------------|-----------|--------------|
| `KeyError: 'Etat'` | Le CSV n'a pas d'en-tête ou les colonnes sont mal nommées. | Vérifie que la première ligne du CSV contient bien les noms des colonnes. |
| `ValueError: invalid literal for int()` | `Durée` n'est pas un entier. | Vérifie que `Durée` est un nombre (ex: `15` et non `"15 min"`). |
| `DoesNotExist: User matching query does not exist` | Un utilisateur n'existe pas. | Crée les utilisateurs manquants ou vérifie `USER_MAP`. |
| `ValueError: time data '02/07/2024' does not match format` | Format de date incorrect. | Vérifie que les dates sont bien au format `JJ/MM/AAAA`. |
| `AttributeError: 'NoneType' object has no attribute 'add'` | `memo.who` est `None`. | Vérifie que `memo` est bien créé avant d'ajouter des utilisateurs. |

---

---

## **🎯 Solution finale recommandée :**
1. **Utilise le script `import_memos.py`** avec les mappages adaptés à ton projet.
2. **Teste avec un petit extrait de ton CSV** avant d'importer tout.
3. **Vérifie les données importées** dans l'admin Django (`/admin/journaling/memo/`).

---
---
## **📝 Résumé des commandes :**
| Commande | Description |
|----------|-------------|
| `uv run python manage.py import_memos data/memos.csv` | Importe les memos depuis un CSV. |
| `uv run python manage.py shell` | Ouvre un shell Django pour vérifier les données. |
| `uv add pandas` | Installe pandas pour un import plus robuste (optionnel). |

---
---
### **Besoin d'aide supplémentaire ?**
- **Veux-tu que je t'aide à :**
  - **Adapter les mappages (`STATE_MAP`, `PRIORITY_MAP`, etc.)** à ton modèle exact ?
  - **Gérer des cas spécifiques** (ex: champs personnalisés, relations complexes) ?
  - **Automatiser l'import régulier** (ex: via une tâche cron) ?