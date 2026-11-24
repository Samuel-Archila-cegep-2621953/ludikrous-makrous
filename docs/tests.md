---
layout: default
title: Tests
---

# Tests

## Premier test: connexion

Pour la connexion, le client envoie un paquet « ping » et porte attention s'il reçoit un paquet en format JSON contenant les informations du serveur. Ensuite, le client envoie les identifiants et le serveur confirme si le compte existe et/ou le client est déjà connecté. S'il est déjà connecté, il envoie un paquet « déconnexion ».

## Deuxième test: obstacles

Pour s'assurer que les obstacles soient les même, on a mis un affichage à chaque fois que le serveur envoie un obstacle. Ensuite, on validait si les valeurs dans le client était le même que celui des autres clients. Un des problèmes était que les client recevait tout le temps les obstacles en retard, et il y avait des joueurs avec des obstacles en avance.

## Troisième test: joueurs

Pour s'assurer que le serveur envoie les positions des joueurs correctement, deux joueurs sont connectés au serveur. Avec le `niveau_debogage` à `5`, on peut comparer la position du `Joueur A` que reçoit le serveur avec celle que reçoit `Joueur B` dans le client. La position était originalement en `float`, mais il y avait des erreurs où `NaN` était interprété par le client. Pour résoudre ce problème, nous avons changé la positioon pour un `int32_t` qui est ensuite divisé du côté du client. Après ce changement, les positions reçues et envoyées correspondaient parfaitement

[Retour](index.md)
