## Devapps - Documentation

### Version de relecture: 0.6.0

### Description

L'application vise à gérer des projets de développement informatique. Elle est accessible depuis SecretBox par l'administrateur.

### Fonctionalités

- CRUD operations et filtres
- Automatise les étapes de création d'une nouvelle version
- Affiche les statistiques de développement

### cas d'utilisation

#### acces au tableau de bord

Depuis la page d'accueil du projet secretbox, si je suis membre du groupe devapps, je dispose d'une icone clickable dans la barre de navigation de gauche pour accéder à l'application devapps.
Si je ne suis pas membre du groupe devapps, l'icone n'est pas visible, l'url m'indique un accès interdit.

#### contenu du tableau de bord

Quand je suis sur la page d'accueil de l'application devapps, je peux voir le tableau contenant la liste des actions répertoriées.
Pour chaque action, je visualise le nom de l'application, la version, la catégorie, la description, les détails, la priorité, l'état, le temps estimé, le temps réalisé, la date de début et fin, un indicateur de planification, l'action supprimé.
Je dispose d'un bouton + pour ajouter une nouvelle action et d'un bouton pour retrier les données.

#### j'ajoute une nouvelle action

Depuis l'accueil de l'application devapps, je clique sur le bouton + dans la barre de navigation horizontale.
Une nouvelle ligne est automatiquement insérée avec:
- application: secretbox
- catégorie: analyse
- description: nouvelle action
- priorité: 100
- état: à faire
- estimé: 0
- planifié: non

#### je modifie une action

Depuis l'accueil de l'application devapps, j'accède directement aux enregistrements en modification. Je peux modifier chaque champs. Je peux modifier le temps réalisé qui peut être également représentée sous la forme d'une addition. 

#### je trie les données

Depuis l'accueil de l'application devapps, je peux cliquer sur le bouton de tri dans la barre de navigation horizontale. Le tableau est automatiquement trier par version ascendant, début descendant, status ascendant, priorité ascendant.

#### je supprime une action

La supprission d'une donnée du tableau de bord devapps n'est pas disponible. Cependant, il est possible de modifier son statut à "annulé".

#### scénario de création-finalisation d'une version

Depuis l'accueil de l'application devapps, je peux cliquer sur le bouton d'initialisation d'une version depuis la barre de navigation horizontale. Une popup me permet de creer une version et de renseigner son objectif. Par défaut, le système me propose de créer les actions standards minimales pour générer une version:
analyse, formation, tests, qualité, documentation utilisateur, documentation technique, déploiement, tests de production.
Je peux ensuite assigner des actions à cette version pour un maximum estimé à 600 minutes. 

#### accés aux statistiques

Depuis l'accueil de l'application devapps, je clique sur le bouton statistique dans la barre de navigation du haut pour accéder à la page des statistiques. Je visualise un cadre pour chaque application contenant le nombre d'actions en cours, un compteur des realisations de l'années. Le nombre d'actions en cours + réalisations sur l'année en cours détermine l'ordre d'affichage des blocs. Je peux également voir la fréquence des réalisations quotidienne comme dans github.
