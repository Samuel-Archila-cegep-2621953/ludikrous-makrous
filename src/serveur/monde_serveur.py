import random
from type_obstacle import TypeObstacle
from obstacle import Obstacle
import constantes
from signal_serveur_client import SignalServeurClient
#import client.joueur
from joueur_abstrait import JoueurAbstrait
import joueur_abstrait

import json
import time

class MondeServeur:
    def __init__(self):
        dimensions = [8,8] # grille 8 x 8
        self.__difficulte_globale = 0
        self.__dimensions: list[int] = dimensions # grandeur de la grille, par défaux 8x8
        self.__joueurs: list[JoueurAbstrait] = [] # Liste de joueurs
        self.__liste_modificateur = []
        self.__temps_de_jeu = 0.0
        self.__partie_en_cours = False

        self.__liste_messages = []

        self.__liste_obstacle = []
        self.__derniere_id = 0

        self.__REQUETES = {
            'CREER ID': self.__recevoir_creer_id,
            'MAJ': self.__recevoir_maj
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

        return _fichier_json

    def __demarrer_nouvelle_partie(self):
        """
        Commencer une nouvelle partie
        """

        self.__difficulte_globale = 0.0
        self.__temps_de_jeu = 0.0
        self.__partie_en_cours = True
        self.effacer_tout_obstacle()

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

    def recevoir_client(self, requete: str) -> str:
        """
        accepter les données du client
        Args:
            requete (str): l'entrée
        Returns:
            str: la sortie du serveur
        """
        _donnee = json.loads(requete)
        return self.__REQUETES[_donnee['Type']](_donnee)
        

    
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
        self.__difficulte_globale += (temps_entre_update * 0.1) #formule linéaire, nombres surement à changer
        # TODO Changer la formule pour augmenter la difficulté

    def __effacer_tout_obstacle(self):

        for o in self.__liste_obstacle:
            o.detruire()

        self.__liste_obstacle = []

        #TODO delete tout les obstacles




    


    
    