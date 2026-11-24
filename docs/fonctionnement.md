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

[Retour](index.md)
