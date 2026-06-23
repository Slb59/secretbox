"""Lists of values used as choices in Django template fields.

This file centralizes type constants (value, label)
to ensure consistency between models, forms and display.
"""

PRIORITY_CHOICES = [
    ("6-lowest", "Très faible"),
    ("5-low", "Faible"),
    ("4-normal", "Normale"),
    ("3-medium", "Moyenne"),
    ("2-high", "Élevée"),
    ("1-highest", "Très élevée"),
]

PERIODIC_CHOICES = [
    ("01-none", "une seule fois"),
    ("02-everyday", "Tous les jours"),
    ("03-every2days", "Tous les 2 jours"),
    ("04-every3days", "Tous les 3 jours"),
    ("05-every4days", "Tous les 4 jours"),
    ("06-every5days", "Tous les 5 jours"),
    ("07-everyweek", "Toutes les semaines"),
    ("08-every10days", "Tous les 10 jours"),
    ("09-every2weeks", "Toutes les 2 semaines"),
    ("10-every3weeks", "Toutes les 3 semaines"),
    ("11-everymonth", "Tous les mois"),
    ("12-every6weeks", "Toutes les 6 semaines"),
    ("13-every2months", "Tous les 2 mois"),
    ("14-every3months", "Tous les 3 mois"),
    ("15-every4months", "Tous les 4 mois"),
    ("16-every6months", "Tous les 6 mois"),
    ("17-everyyear", "Tous les ans"),
    ("18-every18months", "Tous les 18 mois"),
    ("19-every2years", "Tous les 2 ans"),
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
