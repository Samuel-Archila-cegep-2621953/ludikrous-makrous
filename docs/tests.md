---
layout: default
title: Tests
---

# Tests

## Premiers tests: connexion

Pour la connexion, le client envoie un paquet « ping » et porte attention s'il reçoit un paquet en format JSON contenant les informations du serveur. Ensuite, le client envoie les identifiants et le serveur confirme si le compte existe et/ou le client est déjà connecté. S'il est déjà connecté, il envoie un paquet « déconnexion ».

## Deuxièmes tests: obstacles

Pour s'assurer que les obstacles soient les même, on a mis un affichage à chaque fois que le serveur envoie un obstacle. Ensuite, on validait si les valeurs dans le client était le même que celui des autres clients. Un des problèmes était que les client recevait tout le temps les obstacles en retard, et il y avait des joueurs avec des obstacles en avance.

[Retour](index.md)
