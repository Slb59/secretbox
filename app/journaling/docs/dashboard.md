# Le tableau de bord

## Fonctionnement

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

## Coloriser les memos [TODO]

Les memos (une ligne du tableau) sont colorisés en fonction de la priorité, la périodicité, la catégorie, le lieu.