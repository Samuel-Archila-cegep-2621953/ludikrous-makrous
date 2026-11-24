---
layout: default
title: Fonctionnement
---

# Fonctionnement

Le jeu fait présence de plusieurs concepts pythons. Parmi ceux-ci, voici certains:
- Communications client-serveur
- Manipulation de données en plusieurs formats
- Débogage
- Affichage 3D et interfaces graphiques

## Comment le code marche?

Premièrement, les communications client-serveur. Tout d'abord, le client envoie un ping au serveur pour valider son existence. Cela peut se faire en envoyant un message en `bytes` qui est ` b"ping"`. Le serveur renvoie un message en format JSON pour obtenir le nom du serveur et sa description. Ensuite, le client envoie un paquet de connexion ou d'inscription, contenant un pseudonyme avec une longueur maximale de 16 caractères et un mot-de-passe haché avec [SHA-256](https://en.wikipedia.org/wiki/SHA-2), ce qui donnera une clé générée avec [urandom](https://manpages.debian.org/testing/manpages-fr/urandom.4.fr.html) comme *token* d'identification. Après, le client envoie continuellement chaque douzième de seconde sa : position, rotation, *token* d'identification, animation (non implémenté) et sa vie. Le serveur va ensuite envoyer tous les paquets nécessaires pour le jeu, tels que les positions des joueurs, les obstacles et tant d'autres. Finalement, le client va envoyer un paquet de déconnexion pour fermer sa session.

Deuxièmement, le côté serveur. En premier lieu, le serveur reçoit les paquets du client – ce qui va être trié pour mettre à jour toutes les données. En deuxième lieu, le serveur va construire des paquets individuels pour chaque modification. Telle modification peut être : changer de position, nouveaux obstacles. En troisième lieu, le serveur combine chaque paquet, mets une mise en tête, et l'envoie au client pour qu'il le décode.

Troisièmement, le décodage du client. Dans un premier temps, la mise en tête est décodé. Elle contient une `unsigned short` disant le nombre de paquets. Ensuite une boucle `for` en *range* du nombre de paquet est créé. En premier, le programme lit le premier *byte*, ceci est le type de paquet. En second, il lit le reste du paquet, ceci est les données.

Quatrièmement, les interactions des paquets. Chaque paquet appelle une fonction. Par exemple – quand il y a un paquet de missile – le client va placer un missile dans la position X et Y de la carte, et créer une `ursina.Entity` étant le missile. Pour les joueurs – quand il y a un joueur de connecté – le client vérifie si le client existe. S'il existe, le client va simplement mettre à jour les valeurs de ce joueur, telle que la position. Sinon, le client va ajouter le joueur dans la liste des joueurs. 

## Manipulations en plusieurs formats

Parmi tous les formats pour emmagasiner des données, nous avons utilisé trois façons :
- sqlite3
- JSON
- TOML

SQLite3 fut utilisé comme base de donnée pour les comptes dans le jeu et les traductions. En effet, il était plus facile de mettre les traductions dans une base de donnée, à cause qu'il y a des éditeurs comme *Microsoft Excel* pour les bases de données. Ceci rendait la lecture plus facile. JSON fut utilisé pour sauvegarder des configurations qui change tout le temps. Par exemple, l'IP du serveur et les identifiants d'un compte. TOML fut utilisé pour les configurations statiques, par exemple pour l'adresse IP du serveur, le port, le nom et la description.

## Débogage

Malgré le manque de tests, il a fallu beaucoup de débogage, car il y avait constamment des erreurs. En effet, il y avait des erreurs surtout dans les paquets. Par exemple, le *endian* n'était pas correct, etc.

## Affichage 3D

Pour afficher en 3D, *Ursina* a été utilisé. C'est un *game engine* (Moteur de jeu) qui permet de simplifier la programmation graphique en 3D. Ceci avait déjà :
- Un système d'entité
- Un système de mouvement
- Un système pour charger des textures / modèles

Malgré le système déjà existant pour le mouvement, il a été modifié pour être plus fluide.

[Retour](index.md)
