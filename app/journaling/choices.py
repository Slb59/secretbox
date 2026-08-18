"""Lists of values used as choices in Django template fields.

This file centralizes type constants (value, label)
to ensure consistency between models, forms and display.
"""

PRIORITY_CHOICES = [
    ("6-lowest", "6-Le soir"),
    ("5-low", "5-Faible"),
    ("4-normal", "4-Normale"),
    ("3-medium", "3-Moyenne"),
    ("2-high", "2-Élevée"),
    ("1-highest", "1-Le matin"),
]

PERIODIC_CHOICES = [
    ("01-none", "01-une seule fois"),
    ("02-everyday", "02-Tous les jours"),
    ("03-every2days", "03-Tous les 2 jours"),
    ("04-every3days", "04-Tous les 3 jours"),
    ("05-every4days", "05-Tous les 4 jours"),
    ("06-every5days", "06-Tous les 5 jours"),
    ("07-everyweek", "07-Toutes les semaines"),
    ("08-every10days", "08-Tous les 10 jours"),
    ("09-every2weeks", "09-Toutes les 2 semaines"),
    ("10-every3weeks", "10-Toutes les 3 semaines"),
    ("11-everymonth", "11-Tous les mois"),
    ("12-every6weeks", "12-Toutes les 6 semaines"),
    ("13-every2months", "13-Tous les 2 mois"),
    ("14-every3months", "14-Tous les 3 mois"),
    ("15-every4months", "15-Tous les 4 mois"),
    ("16-every6months", "16-Tous les 6 mois"),
    ("17-everyyear", "17-Tous les ans"),
    ("18-every18months", "18-Tous les 18 mois"),
    ("19-every2years", "19-Tous les 2 ans"),
]

CATEGORY_CHOICES = [
    ("01-organisation", "Organisation"),
    ("02-compta", "Compta"),
    ("03-achat", "Achats"),
    ("04-sport", "Sport"),
    ("05-sante", "Santé"),
    ("06-contact", "Contact"),
    ("07-informatique", "Informatique"),
    ("08-menage", "Menage"),
    ("09-jardin", "Jardin"),
    ("10-doudou", "Doudou"),
    ("11-bricoles", "Bricoles"),
    ("12-couture", "Couture"),
    ("13-loisirs", "Loisirs"),
    ("14-vacances", "Vacances"),
]

PLACE_CHOICES = [
    ("cantin-ext", "Cantin exterieur"),
    ("cantin-int", "Cantin interieur"),
    ("chm", "CHM"),
    ("genese", "Genèse"),
    ("fontaine", "Fontaine"),
]

ACTION_CHOICES = [
    ("created", "Création"),
    ("updated", "Mise à jour"),
    ("deleted", "Suppression"),
    ("restored", "Restauration"),
]
