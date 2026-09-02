## Journaling - Documentation

### Version de relecture : 0.5.0

### Description

Journalling propose la liste des actions à réaliser dans la journée et planifie le reste des actions et évènements.

### Le tableau de bord

J'appelle memo une action du tableau de bord.
Les données du tableau de bord sont:

état: à faire, terminé, annulé
durée: entre 10 and 800, defaut:30
description: détail de l'opération à effectuer
rendez-vous: rendez-vous, anniversaire, fête
type: Liste de valeur finie (à mettre en paramètres)
qui: par défaut l'utilisateur connecté - plusieurs valeurs possibles
lieu: Liste de valeur (à mettre en paramètres)
periodique: Liste de valeur (à mettre en paramètres)

planifié: date planifiée, défaut= date du jour +1, 
	la date est recalculée en fonction de la périodicité à chaque fois qu'un mémo est validé.  
priorité: (matin, élevé, moyenne, normal, faible, soir) défaut= matin

fait: égale à la date du jour lorsque le mémo est réalisé.
note: Une note complémentaire à la description

Les données sont triées par ordre croissant selon : 
la date planifiée, la priorité, la durée, qui, le lieu, la périodicité, la catégorie, la description

### Cycle de vie d'un memo

Exemple :  
memo(planifié 23/06, réalisé: none , report: none, quotidien)
23/06 : le mémo est validé => memo(planifié: 24/06, réalisé: 23/06 , report: none)
24/06 : le mémo est reporté au 28/06 => mémo(planifié: 28/06, réalisé: 23/06 , report: 24/06)
28/06 : le memo est reporté au 30/06 => memo(planifié: 30/06, réalisé: 23/06 , report: 24/06)
30/06 : le mémo est validé => mémo(planifié: 31/06, rélisé: 30/06 , report: none)

#### valider un memo [TODO]
Un bouton pour validation est disponible dans la colonne action uniquement pour les enregistrements avec l'état "à faire".
La nouvelle date de planification est calulée en fonction de la périodicité et proposée en popup avant validation.
La date de réalisation est proposée par défaut à la date du jour. Elle est également modifiable dans la popup.
Sur validation, si la date de report est renseignée, elle est effacée.

#### reporter un memo [TODO]
Un bouton pour report est disponible dans la colonne action, uniquement pour les enregistrement avec l'état "à faire".  
Une popup propose:  
- un champ modifiable avec la date report calculée en fonction de périodicité.
- un bouton de validation et un bouton d'annulation.  

Sur validation la date de planification est modifiée.  
Si la date de report n'est pas renseignée, elle est alimentée avec la date du jour.

#### Commencer une nouvelle journée 

Dans le menu horizontal, en haut de tableau, un bouton permet de "demarrer une journée". Une popup s'ouvre et propose par défaut la date du jour. Je laisse la possibilité de modifier cette date car il arrive que je loupe un journée de suivie. Cette fonction me permet de basculer sur une date choisie.

Sur validation, les statistiques sont mises à jour. (temps cumulé restant de la journée à basculer).

La journée qui sera basculée correspond à la plus ancienne date des éléments à l'état "à faire".

Sur validation, la date de planification est mis à jour pour l'ensemble de ces enregistrements.

Un nouvel enregistrement de satistiques est alors créé avec le cumul des temps et le cumul des temps pour les enregistrements topés "actions du jour" 

Une nouvelle journée peut commencer :D

Evolution possible: enregistrer avec les statistiques une note du jour, le temps qu'il fait, un dicton, à méditer :) 

#### Coloriser les memos [TODO]

Les memos (une ligne du tableau) sont colorisés en fonction de la priorité, la périodicité, la catégorie, le lieu.

#### Supprimer un memo [TODO]

Un bouton de suppression est disponible dans la colonne action. L'enregistrement ne sera pas supprimé de la base de données, l'état est mis à "annulé".

### Améliorations

- Ajouter un chrono/pomodoro (je pense plutôt créer une nouvelle application à moins de l'associer à un enregistrement mais sans un couplage fort. L'un n'empêche pas l'autre)

Il faut que je puisse modifier le temps enregistré quand je stoppe le chrono (car souvent j'oublie de l'arrêter)

Enregistrer le temps réellement effectuer pour une action me permettrait de mieux planifier mes journées.

- Ajouter un case à cocher pour l'action du jour
- Creer une notion de sous-memo
