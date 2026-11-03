import random
from type_obstacle import TypeObstacle
from obstacle import Obstacle
import constantes
from signal_serveur_client import SignalServeurClient
#import client.joueur
from joueur_abstrait import JoueurAbstrait
import joueur_abstrait
import journal
from debogage import Debogage as Dbg

import struct
import json
import time
from modificateur_difficulte import ModificateurDifficulte

from type_paquet import TypePaquetClient
import paquet
import base_de_donnees
import hashlib

import os

class MondeServeur:
    def __init__(self):
        dimensions = [8,8] # grille 8 x 8
        self.base_donnee = base_de_donnees.BaseDeDonnees()
        self.__compteur = 0

        self.__difficulte_globale = 0
        self.__dimensions: list[int] = dimensions # grandeur de la grille, par défaux 8x8
        self.__joueurs: list[JoueurAbstrait] = [] # Liste de joueurs
        self.__joueurs_hache: dict[bytes,int] = {}
        self.__liste_modificateur = []
        self.__temps_de_jeu = 0.0
        self.__partie_en_cours = False

        self.__liste_messages = []

        self.__liste_obstacle = []
        self.__personnes_a_ajoute: list[tuple[int,str]] = []
        self.__derniere_id = 0

        self.__REQUETES = {
            'CREER ID': self.__recevoir_creer_id,
            'MAJ': self.__recevoir_maj
        }
        self.__REQUETES_PAQUETS = {
            TypePaquetClient.MAJ_JOUEUR.value[0]: self.__recevoir_maj_paquets,
            TypePaquetClient.CONNEXION.value[0]: self.__recevoir_connexion_paquets,
            TypePaquetClient.CREATION_COMPTE.value[0]: self.__recevoir_inscrire_paquets
        }
        

    def __formatter_dict(self, joueurs_quitte: list[int]):
        """
        Formatte le monde du serveur en json pour l'envoyer au client.
        Style:
            {
                "Général": {
                    "Temps de jeu": <__temps_de_jeu>,
                    "Liste messages": <SignalServeurClient> 
                },

                "Nouveaux Obstacles": [
                    {
                        "Type": <type>
                        "Position": <position>
                    }
                ],

                "Joueurs": [ # Envoyer en ordre de leur classement selon leur score
                    {
                        "ID": <ID>
                        "Position": <[x, y, x]>,
                        "Nom": <nom>,
                        "Vie": <vie>,
                        "En_vie": <en_vie>
                        "Animation": <animation>
                    }
                }
            }

        """
        _fichier_json = {}

        _fichier_json["Général"] = {}

        _fichier_json["Général"]["Temps de jeu"] = self.__temps_de_jeu

        _liste_message = []
        for m in self.__liste_messages:

            _liste_message.append(m)

            _fichier_json["Général"]["Liste messages"] = self.__liste_messages


        _fichier_json["Nouveaux obstacles"] = []

        for o in self.__liste_obstacle:

            _nouveau_obstacle = {}

            _nouveau_obstacle["Type"] = o.__type_obstacle
            _nouveau_obstacle["Position"] = [o.__position[0], o.__position[1], o.__position[2]]

            _fichier_json["Nouveaux obstacles"].append(_nouveau_obstacle)


        _fichier_json["Joueurs"] = joueur_abstrait.formatter_json(self.__joueurs)

        _fichier_json["Joueurs quittés"] = joueurs_quitte

        Dbg.info(f"Fichier JSON dabs MondeServeur.__formatter_dict: {_fichier_json}", 3)
        return _fichier_json

    def __demarrer_nouvelle_partie(self):
        """
        Commencer une nouvelle partie
        """

        self.__difficulte_globale = 0.0
        self.__temps_de_jeu = 0.0
        self.__partie_en_cours = True
        self.effacer_tout_obstacle()

        Dbg.info("Nouvelle partie commencée", 2)
        self.__liste_message.append("partie_commence")

    def __recevoir_creer_id(self, donnee: dict) -> str:
        _temps = time.time()
        for idx, _ in enumerate(self.__joueurs):
            if _temps - _.dernier_paquet > 10:
                self.__joueurs.remove(_)
        if len(self.__joueurs) == 0: self.__derniere_id = 0
        _joueur = JoueurAbstrait()
        _joueur.id = self.__derniere_id
        self.__joueurs.append(_joueur)
        _resultat = json.dumps({'ID': self.__derniere_id})
        print(f"[+] Joueur {self.__derniere_id}")
        self.__derniere_id += 1
        return _resultat

    def __recevoir_maj(self, donnee: dict) -> str:
        _index_joueur = 0
        for idx, _ in enumerate(self.__joueurs):
            if _.id == donnee['ID']:
                _index_joueur = idx
        self.__joueurs[_index_joueur].position = (
            donnee['Position'][0],
            donnee['Position'][1],
            donnee['Position'][2]
        )


        _temps = time.time()
        self.__joueurs[_index_joueur].dernier_paquet = _temps

        _joueurs_quittes = []
        for idx, _ in enumerate(self.__joueurs):
            if _temps - _.dernier_paquet > 10:
                _joueurs_quittes.append(idx)
                self.__joueurs.remove(_)

        if len(_joueurs_quittes) > 0:
            if len(_joueurs_quittes) == 1:
                print(f"[-] Joueur {_joueurs_quittes[0]}")
            else:
                print(f"[-] Joueurs {_joueurs_quittes}")

        return json.dumps(self.__formatter_dict(_joueurs_quittes))

    def __obtenir_joueur_par_id(self, id: int):
        for _ in self.__joueurs:
            if _.id == id:
                return _
        return None

    def __recevoir_connexion_paquets(self, donnee: tuple) -> bytes:
        """
        Lit un paquet de connexion et envoit une notification de réussite ou d'échec\n
        Entrée: `B16s32s`\n
        Sortie: `B32s` | `B`\n
        """
        _nom = donnee[1].decode().replace('\0', '')
        if self.base_donnee.connexion(_nom, hashlib.sha256(donnee[2]).hexdigest()):
            Dbg.info(f"[+] {_nom} s'est connecté.")
            self.__compteur += 1
            # hashlib c bien mais aléatoire c mieux
            # _clef = hashlib.sha256(str(self.__compteur).encode()).digest()
            _clef = os.urandom(32)
            _id = self.base_donnee.obtenir_id(_nom)

            _joueur = JoueurAbstrait()
            _joueur.id = _id
            self.__joueurs.append(_joueur)

            self.__joueurs_hache[_clef] = _id
            return paquet.construire_paquet([paquet.creer_paquet_connexion_reussit(_clef)])

        Dbg.avis(f"{_nom} a tenté une connexion, hash: {hashlib.sha256(donnee[2]).hexdigest()}")
        return paquet.construire_paquet([paquet.creer_paquet_connexion_rate()])


    def __recevoir_inscrire_paquets(self, donnee: tuple) -> bytes:
        """
        Lit un paquet d'inscription et envoit une notification de réussite ou d'échec\n
        Entrée: `B16s32s`\n
        Sortie: `B32s` | `B`\n
        """
        _nom = donnee[1].decode().replace('\0', '')
        if self.base_donnee.creer_utilisateur(_nom, hashlib.sha256(donnee[2]).hexdigest()):
            self.__compteur += 1
            _clef = hashlib.sha256(str(self.__compteur).encode()).digest()
            _id = self.base_donnee.obtenir_id(_nom)
        
            _joueur = JoueurAbstrait()
            _joueur.id = _id
            self.__joueurs.append(_joueur)
        
            self.__joueurs_hache[_clef] = _id
            return paquet.construire_paquet([paquet.creer_paquet_connexion_reussit(_clef)])
        return paquet.construire_paquet([paquet.creer_paquet_connexion_rate()])

    def __recevoir_maj_paquets(self, donnee: tuple) -> bytes:
        """
        Lit un paquet de mise à jour et envoit une mise à jour de chaque joueurs\n
        Entrée: `B32sfffBB`\n
        Sortie: `H(BIfff16sBB+...)`\n
        """
        if donnee[1] not in self.__joueurs_hache:
            Dbg.avis("Un joueur a tenté de mettre à jour un joueur qui n'existe pas. Ce joueur sera déconnecté.", 1)
            return paquet.construire_paquet([paquet.creer_paquet_deconnexion()])
        _id = self.__joueurs_hache[donnee[1]]

        if (joueur := self.__obtenir_joueur_par_id(_id)) != None:
            joueur.position = (donnee[2], donnee[3], donnee[4])
            joueur.vie = donnee[5]
            joueur.animation = donnee[6]

        _joueurs = [paquet.creer_paquet_joueur(joueur) for joueur in self.__joueurs]
        return paquet.construire_paquet(_joueurs)

    def recevoir_client_paquets(self, requete: bytes) -> bytes:
        _paquet = paquet.lire_paquet(requete)
        _resultat = self.__REQUETES_PAQUETS[_paquet[0]](_paquet)
        Dbg.info(f"Résultat de recevoir_client_paquets: {_resultat}", 2)
        return _resultat


    def recevoir_client(self, requete: str) -> str:
        """
        accepter les données du client
        Args:
            requete (str): l'entrée
        Returns:
            str: la sortie du serveur
        """
        _donnee = json.loads(requete)
        _resultat = self.__REQUETES[_donnee['Type']](_donnee)
        Dbg.info(f"Résultat de recevoir_client: {_resultat}", 2)
        return _resultat

    
    def __terminer_partie(self):
        """
        terminer la partie
        """
        
        
        self.__difficulte_globale = 0.0
        self.__temps_de_jeu = 0.0
        self.__partie_en_cours = False
        self.__effacer_tout_obstacle()

        self.__liste_message.append("partie_fin")


    def mise_a_jour_jeu(self, temps_entre_update: float):

        if self.__partie_en_cours == True:
            
            self.__temps_de_jeu += temps_entre_update

            for obstacle1 in self.__liste_obstacle:

                obstacle1.mise_a_jour(temps_entre_update)
                
            self.__maj_difficulte(temps_entre_update)

            self.__choisir_obstacles()

                
            
    def __joueurs_ordonnes(self) -> list[JoueurAbstrait]:
        """
        Place les joueurs en ordre selon leur score
        """
        _liste_joueurs: list[JoueurAbstrait] = []
        for idx, j in enumerate(self.__joueurs):
            for j_a in _liste_joueurs:
                if j.score > j_a.score:
                    _liste_joueurs.insert(idx, j)
        # TODO tester
                    
                    

    def __difficulte_actuelle(self) -> float:
        """
        Compte les obstacles présents sur la grille et retourne la somme de leurs difficultés
        """
        _difficulte_actuelle = 0.0
        for  o in self.__liste_obstacle:
            _difficulte_actuelle += o.difficulte

        return _difficulte_actuelle


    def __choisir_obstacles(self) -> list[TypeObstacle]:
        _difficulte_cible = self.__difficulte_globale        
        _difficulte_atteinte = 0.0 + self.__difficulte_actuelle()
        _nouveaux_obstacles: list[TypeObstacle] = []

        while _difficulte_atteinte < _difficulte_cible: # Continue à ajouter des obstacles jusqu'à la difficulté globale
            _rand_obstacle: TypeObstacle = random.randint(1, TypeObstacle.max())
            
            _difficulte_atteinte += _rand_obstacle.difficulte
            _nouveaux_obstacles.append(_rand_obstacle)

        return _nouveaux_obstacles
        
        
    def __creer_obstacles(self, nouveaux_obstacles: list[TypeObstacle]):
        # TODO Compléter
        pass

    def __maj_difficulte(self, temps_entre_update: float):
        self.__difficulte_globale += ModificateurDifficulte.fonction_difficulte(constantes.NIVEAU_DIFFICULTE)(temps_entre_update * 0.1)

    def __effacer_tout_obstacle(self):

        for o in self.__liste_obstacle:
            o.detruire()

        self.__liste_obstacle = []

        #TODO delete tout les obstacles




    


    
    