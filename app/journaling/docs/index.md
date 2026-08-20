## Journaling - Documentation

### Version de relecture : 0.4.0

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

### Cycle de vie d'un memo

Exemple :  
memo(planifié 23/06, réalisé: none , report: none, quotidien)
23/06 : le mémo est validé => memo(planifié: 24/06, réalisé: 23/06 , report: none)
24/06 : le mémo est reporté au 28/06 => mémo(planifié: 28/06, réalisé: 23/06 , report: 24/06)
28/06 : le memo est reporté au 30/06 => memo(planifié: 30/06, réalisé: 23/06 , report: 24/06)
30/06 : le mémo est validé => mémo(planifié: 31/06, rélisé: 30/06 , report: none)

#### reporter un memo
Dans la div d'actions, je voudrais avoir un bouton en forme de flèche pointant vers la droite (le design de l'icône reste à faire).  
Lorsque je clique sur cette icône, une fenêtre contextuelle (popup) s'ouvre.  
Un champ modifiable me propose une date de report calculée par la fonction `todo.next_date()`.  
Cette popup contient également un bouton de validation et un bouton d'annulation.  
Si je valide, la date `todo.planned_date` est écrasée par la date proposée ou modifiée.  
Si `todo.report_date` n'est pas spécifiée, elle est mise à jour avec la date du jour.  
Seuls les éléments avec `todo.state='Todo'` peuvent avoir ce comportement.  
Je dois également modifier le comportement du bouton de validation pour que, lorsqu'un élément est validé, `todo.report_date` soit définie à `null`.

#### Reporter tous les memos au jour suivant

At the start of the day, I start by closing the previous day. I note the time not completed for statistical purposes to have time completed – time remaining = time completed. Then I select all items that have scheduled_date on today's date and bring them forward to the next day. I redo a selection of the elements of the day, that is to say the elements that I have just postponed + the elements already programmed, to note the time to be allocated in the statistics of the day. The day can begin. I would also like to record the weather that was during the day and during this report.

#### Coloriser les memos

I would like to define a parameter table to set a color for a combination of priority, periodicity, category and place.  
I group the data like this way:  
Priority:  
higest-hight
medium-normal
low, lowest
Periodicity:
every day, every 2 days, every 3 days
none
every 4 days, 5 days, week
every 10 days, 2 weeks
every 3 weeks, 1 month, 2 month
every 3 month, 6 month, a year
category:
organisation, contact, doudou
compta, achat
sport, santé
informatique
menage, jardin
bricoles, couture, loisirs
place
cantin
genese
chm

there are therefore a total of 432 possibilities (3*6*6*4)

#### Supprimer un memo

From the dashboard, for each operation, I can perform a deletion. In the actions column, a link allows me to access this function. The item is not actually deleted. The status is set to “canceled”. The cancellation is recorded in the operation's modification history.

### Améliorations

- Ajouter un chrono/pomodoro

I would like to set up a stopwatch function on my dashboard. That is to say that in the actions div, with the edit and delete links I will have a link to activate the stopwatch. When I click on this link, the link turns into flashing. Between the filter and the table then appears a line containing the name of the current task, the time scroll and the stop button. When I activate the stop button, the timer stops, a popup offers me the time to save which I can possibly modify. I can either cancel the operation or validate it. If I validate, the time is recorded in a history with start date + validated time. This history will then be visible when hovering over the status column.


- Ajouter un case à cocher pour l'action du jour
- Creer une notion de sous-memo
