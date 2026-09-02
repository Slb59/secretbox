## Dictavoix - Documentation

### Version de relcture: 0.5.0

### Description

DictaVoix est une application du projet SecretBox. L'idée est de générer un audio qui permet de dicter le texte proposé. 

L'accès se fait via le tableau de bord SecretBox en fonction des droits utilisateurs.

Une première lecture à vitesse normale est effectuée puis chaque phrase est redite 4 fois lentement avec ponctuation. Enfin le texte est redit lentement avec ponctuation puis à vitesse normale.

Un dictionnaire de mots difficiles est sauvegardé dans la base de données.
Les mots du dictionnaire peuvent être répétés.

Les dictées sont sauvegardés dans la base de données. On pourra également sauvegarder le résultat de la dictée (nombre d'erreur / nombre de mots / nombre de mots du dictionnaire)