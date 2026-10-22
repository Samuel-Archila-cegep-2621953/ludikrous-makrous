import random
from type_obstacle import TypeObstacle
from obstacle import Obstacle
import constantes
from signal_serveur_client import SignalServeurClient
#import client.joueur
from joueur_abstrait import JoueurAbstrait
import joueur_abstrait

import json

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

        self.__REQUETES = {
            'CREER ID': self.__recevoir_creer_id,
            'MAJ': self.__recevoir_maj
        }
        

    def __formatter_dict(self):
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
                        "Position": <[x, y, x]>,
                        "Nom": <nom>,
                        "Vie": <vie>,
                        "Animation": <animation>
                    }
                ]
            }

        """
        fichier_json = {}

        fichier_json["Général"] = {}

        fichier_json["Général"]["Temps de jeu"] = self.__temps_de_jeu

        liste_message = []
        for m in self.__liste_messages:

            liste_message.append(m)

            fichier_json["Général"]["Liste messages"] = self.__liste_messages


        fichier_json["Nouveaux obstacles"] = []

        for o in self.__liste_obstacle:

            nouveau_obstacle = {}

            nouveau_obstacle["Type"] = o.__type_obstacle
            nouveau_obstacle["Position"] = [o.__position[0], o.__position[1], o.__position[2]]

            fichier_json["Nouveaux obstacles"].append(nouveau_obstacle)


        fichier_json["Joueurs"] = joueur_abstrait.formatter_json(self.__joueurs)

        return fichier_json

    def demarrer_nouvelle_partie(self):
        """
        Commencer une nouvelle partie
        """

        self.__difficulte_globale = 0.0
        self.__temps_de_jeu = 0.0
        self.__partie_en_cours = True
        self.effacer_tout_obstacle()

        self.__liste_message.append("partie_commence")

    def __recevoir_creer_id(self, donnee: dict) -> str:
        _nombre_joueur = len(self.__joueurs)
        _joueur = JoueurAbstrait()
        _joueur.id = _nombre_joueur
        self.__joueurs.append(_joueur)
        return json.dumps({'ID': _nombre_joueur})

    def __recevoir_maj(self, donnee: dict) -> str:
        self.__joueurs[donnee['ID']].position = (
            donnee['Position'][0],
            donnee['Position'][1],
            donnee['Position'][2]
        )
        return json.dumps(self.__formatter_dict())

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
        

    
    def terminer_partie(self):
        """
        terminer la partie
        """
        
        
        self.__difficulte_globale = 0.0
        self.__temps_de_jeu = 0.0
        self.__partie_en_cours = False
        self.effacer_tout_obstacle()

        self.__liste_message.append("partie_fin")


    def mise_a_jour_jeu(self, temps_entre_update: float):

        if self.__partie_en_cours == True:
            
            self.__temps_de_jeu += temps_entre_update

            for obstacle1 in self.__liste_obstacle:

                obstacle1.mise_a_jour(temps_entre_update)
                
            self.maj_difficulte(temps_entre_update)

            self.choisir_obstacles()

                
            
    def joueurs_ordonnes(self) -> list[JoueurAbstrait]:
        """
        Place les joueurs en ordre selon leur score
        """
        liste_joueurs: list[JoueurAbstrait] = []
        for idx, j in enumerate(self.__joueurs):
            for j_a in liste_joueurs:
                if j.score > j_a.score:
                    liste_joueurs.insert(idx, j)
        # TODO tester
                    
                    

    def difficulte_actuelle(self) -> float:
        """
        Compte les obstacles présents sur la grille et retourne la somme de leurs difficultés
        """
        difficulte_actuelle = 0.0
        for o in self.__liste_obstacle:
            difficulte_actuelle += o.difficulte

        return difficulte_actuelle


    def choisir_obstacles(self) -> list[TypeObstacle]:
        difficulte_cible = self.__difficulte_globale        
        difficulte_atteinte = 0.0 + self.difficulte_actuelle()
        nouveaux_obstacles: list[TypeObstacle] = []

        while difficulte_atteinte < difficulte_cible: # Continue à ajouter des obstacles jusqu'à la difficulté globale
            rand_obstacle: TypeObstacle = random.randint(1, TypeObstacle.max())
            
            difficulte_atteinte += rand_obstacle.difficulte
            nouveaux_obstacles.append(rand_obstacle)

        return nouveaux_obstacles
        
        
    def creer_obstacles(self, nouveaux_obstacles: list[TypeObstacle]):
        # TODO Compléter
        pass

    def maj_difficulte(self, temps_entre_update: float):
        self.__difficulte_globale += (temps_entre_update * 0.1) #formule linéaire, nombres surement à changer
        # TODO Changer la formule pour augmenter la difficulté

    def effacer_tout_obstacle(self):

        for o in self.__liste_obstacle:
            o.detruire()

        self.__liste_obstacle = []

        #TODO delete tout les obstacles




    


    
    