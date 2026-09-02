## Account - Documentation

### Version de relcture: 0.5.0

### Objectif
Cette application gère les comptes d'accès et autorisations

### Fonctionnalités

A l'ouverture de l'application, l'utilisateur non connecté accède à la page de connexion. Il peut s'identifier avec son email et son mot de passe.
Si le compte est reconnu, il est redirigé sur son tableau de bord. (Application Journaling)
Sinon, il peut reinitialiser son mot de passe ou contacter l'administrateur pour modifier son email.

Il y a un compte administrateur (osynia).

#### Demande de changement de mot de passe
Elle peut se faire depuis la page de connexion ou depuis la page profile.
L'utilisateur doit saisir son email pour obtenir l'accès à la page de reinitialisation de son mot de passe. Sur la page de reinitialisation, il peut saisir son nouveau mot de passe avec confirmation. Il est alors redirigé vers la page de connexion.

#### Suppression de compte
Seul l'administration a la possibilité de supprimer un compte. Ceci est compliqué car il anonymise toutes les relations avec le compte.

#### Modification des données personnelles
L'accès aux données personnelles peut se faire depuis toutes les pages de l'application. (Lien sur photo de profile).
Il peut modifier la photo de profile, son nom d'usage, reinitialiser son mot de passe, effectuer une demande de changement email à l'administrateur.
La page profile montre également des statistiques sur l'usage de l'application (nombre de tâches en cours, liste des applications accéssibles)
