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
from tuile import Tuile

import struct
import json
import time
from modificateur_difficulte import ModificateurDifficulte

from type_paquet import TypePaquetClient, TypePaquetServeur
import paquet
import base_de_donnees
import hashlib

import os

from collections.abc import Callable

from obstacles import (laser, pilier, reservation, train, vague, missile)
import math

class MondeServeur:
    def __init__(self):
        dimensions = [8,8] # grille 8 x 8
        self.base_donnee = base_de_donnees.BaseDeDonnees()
        self.__compteur = 0

        self.__difficulte_globale = 0
        self.__tuiles: list[list] = [] # grandeur de la grille, par défaux 8x8

        for i in range(dimensions[0]):
            self.__tuiles.append([])
            for _ in range(dimensions[1]):
                self.__tuiles[i].append(None)

        self.__joueurs: list[JoueurAbstrait] = [] # Liste de joueurs
        self.__joueurs_hache: dict[bytes,int] = {}
        self.__liste_modificateur = []
        self.__temps_de_jeu = 0.0
        self.__partie_en_cours = True

        self.__liste_messages = []


        self.__liste_obstacle: list[Obstacle] = []
        self.__personnes_a_ajouter: list[tuple[int,str]] = []
        self.__derniere_id = 0
        self.__nouveaux_obstacles: list[bytes] = []
        self.__joueurs_auxquels_envoyer_obstacles: list[int] = []
        self.__debut = time.time()
        self.__moment_maj_anterieure: float = self.__debut
        self.__lock = False
        self.__obstacles_implementes = [TypeObstacle.PILIER.value, TypeObstacle.RIEN.value, TypeObstacle.MISSILE.value]

        #self.

        self.niveau_difficulte = 3

        """ OBSOLÈTE
        self.__REQUETES = {
            'CREER ID': self.__recevoir_creer_id,
            'MAJ': self.__recevoir_maj
        }
        """
        self.__REQUETES_PAQUETS = {
            TypePaquetClient.MAJ_JOUEUR.value[0]: self.__recevoir_maj_paquets,
            TypePaquetClient.CONNEXION.value[0]: self.__recevoir_connexion_paquets,
            TypePaquetClient.CREATION_COMPTE.value[0]: self.__recevoir_inscrire_paquets,
            TypePaquetClient.DECONNEXION.value[0]: self.__recevoir_deconnexion_paquets,
        }

    def __obtenir_joueur_par_id(self, id: int):
        for j in self.__joueurs:
            if j.id == id:
                return j
        return None

    def __recevoir_deconnexion_paquets(self, donnee: tuple) -> bytes:
        for i, _ in enumerate(self.__joueurs):
            if _.id == self.__joueurs_hache[donnee[1]]:
                del self.__joueurs[i]
        del self.__joueurs_hache[donnee[1]]
        return paquet.construire_paquet([paquet.creer_paquet_connexion_rate()])

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

            for _it_clef, _it_id in self.__joueurs_hache.items():
                if _it_id == _id:
                    return paquet.construire_paquet([paquet.creer_paquet_connexion_rate()])

            _joueur = JoueurAbstrait()
            _joueur.id = _id
            self.__joueurs.append(_joueur)

            self.__joueurs_hache[_clef] = _id
            return paquet.construire_paquet([paquet.creer_paquet_connexion_reussit(_clef, _id)])

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
            Dbg.info(f"[+] {_nom} s'est connecté.")
            self.__compteur += 1
            _clef = hashlib.sha256(str(self.__compteur).encode()).digest()
            _id = self.base_donnee.obtenir_id(_nom)
        
            _joueur = JoueurAbstrait()
            _joueur.id = _id
            self.__joueurs.append(_joueur)
        
            self.__joueurs_hache[_clef] = _id
            return paquet.construire_paquet([paquet.creer_paquet_connexion_reussit(_clef, _id)])
        return paquet.construire_paquet([paquet.creer_paquet_connexion_rate()])

    def __recevoir_maj_paquets(self, donnee: tuple) -> bytes:
        """
        Lit un paquet de mise à jour et envoit une mise à jour de chaque joueur\n
        Entrée: `B32siiiBB`\n
        Sortie: `H(BIiii16sBB+...)`\n
        """
        if donnee[1] not in self.__joueurs_hache:
            Dbg.avis("Un joueur a tenté de mettre à jour un joueur qui n'existe pas. Ce joueur sera déconnecté.", 1)
            return paquet.construire_paquet([paquet.creer_paquet_deconnexion()])
        _id = self.__joueurs_hache[donnee[1]]

        if (joueur := self.__obtenir_joueur_par_id(_id)) != None:
            joueur.position = (donnee[2], donnee[3], donnee[4])
            joueur.vie = donnee[5]
            joueur.animation = donnee[6]
            #joueur.a_recu_maj_obstacles()


        _joueurs: list[bytes] = [paquet.creer_paquet_joueur(joueur) for joueur in self.__joueurs]
        #print("here")

        #TEMPS_UPDATE: float = 0.01
        #self.__temps_de_jeu += TEMPS_UPDATE
        #self.__nettoyer_tuiles()
        #self.__creer_obstacles()
        self.__maj_difficulte()
        #self.__difficulte_globale += 0.2
        #self.maj_compteur()
        #self.mise_a_jour_jeu(None)


        #return paquet.construire_paquet(_joueurs)
        #if len(self.__nouveaux_obstacles) != 0: print("OBSCTALEES")


        #_joueurs + self.__nouveaux_obstacles if not self.__obtenir_joueur_par_id(_id).a_recu_maj_obstacles() else _joueurs
        _joueur = self.__obtenir_joueur_par_id(_id)
        if _joueur.doit_recevoir_maj_obstacles: 
            _paquet_final = paquet.construire_paquet(_joueurs + self.__nouveaux_obstacles)
            _joueur.a_recu_maj_obstacles()
        else: _paquet_final = paquet.construire_paquet(_joueurs)
            #_joueurs + self.__nouveaux_obstacles if not self.__obtenir_joueur_par_id(_id).a_recu_maj_obstacles() else _joueurs
        
        


        #print(len(self.__nouveaux_obstacles))

        if len(self.__nouveaux_obstacles) > 0:
            Dbg.info(f"Ajout de {len(self.__nouveaux_obstacles)} obstacle(s)", 3)
            Dbg.info(f"MondeServeur::__recevoir_maj_paquets: Nouveaux obstacles comme bytes {self.__nouveaux_obstacles}", 5)
            #Dbg.info(f"MondeServeur::__recevoir_maj_paquets: len(self.__nouveaux_obstacles) = {len(self.__nouveaux_obstacles)}")

        """
        if self.__lock == False:
            #print("No lock")
            self.__lock = True
            #self.__nouveaux_obstacles = []
            self.__lock = False
        """

        return _paquet_final

    def recevoir_client_paquets(self, requete: bytes) -> bytes:
        _paquet = paquet.lire_paquet(requete)
        _resultat = self.__REQUETES_PAQUETS[_paquet[0]](_paquet)
        Dbg.info(f"Résultat de recevoir_client_paquets: {_resultat}", 5)
        return _resultat

    def joueurs(self) -> list:
        return [f'{j.id} {j.position[0] / 100}, {j.position[1] / 100}, {j.position[2] / 100}' for j in self.__joueurs]

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


    def mise_a_jour_jeu(self):
        #Dbg.info("Maj jeu")

        if self.__partie_en_cours == True:
            
            #self.__temps_de_jeu += temps_entre_update

            """
            for obstacle in self.__liste_obstacle:

                obstacle1.mise_a_jour(temps_entre_update)
            """
            #Dbg.info(f"tt{temps_entre_update}", 3)

            self.nettoyer_tuiles()
            Dbg.info("Dans MondeServeur::mise_a_jour_jeu()")
            self.__maj_difficulte()
            self.creer_obstacles()
            #self.maj_compteur()

    def maj_compteur(self, max = 50):
        MAX_COMPTEUR: int = max
        self.__compteur += 1
        if self.__compteur == MAX_COMPTEUR: self.__compteur = 0
            
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


    def creer_obstacles(self):

        #if self.__compteur != 0: 
        if self.__decider_si_cycle() == False:
            #Dbg.info(str(self.__compteur), 4)
            #return
            pass

        if self.__lock == True:  return

        self.__lock = True

        _difficulte_cible = self.__difficulte_globale        
        _difficulte_atteinte = 0.0 + self.__difficulte_actuelle()
        #_nouveaux_obstacles: list[TypeObstacle] = []

        MAX_LOOPS = 48

        #_i = 0
        #while _difficulte_atteinte < _difficulte_cible or _i > MAX_LOOPS: # Continue à ajouter des obstacles jusqu'à la difficulté globale
        for _ in range(MAX_LOOPS): #NOTE il faut placer une limite explicite au nombre de fois que l'algorithme peut essayer de générer des obstacles pour éviter que le serveur bloque
            if _difficulte_atteinte > _difficulte_cible : break
            #_i += 1
            _rand_obstacle: int = random.randint(0, TypeObstacle.max())

            if _rand_obstacle == TypeObstacle.RIEN.value:
                _chance = random.randint(0, 2)
                if _chance != 0:
                    continue

            #if _rand_obstacle != TypeObstacle.PILIER.value or _rand_obstacle != TypeObstacle.RIEN.value:
            #if not (_rand_obstacle == TypeObstacle.PILIER.value or _rand_obstacle == TypeObstacle.RIEN.value):
            if not _rand_obstacle in self.__obstacles_implementes:
                #print("pas pilier")
                continue # HACK: Les autres obstacles n'existent pas encore
            
            _fn_creer_obstacle: Callable = MondeServeur.__constructeur_obstacle_depuis_type(_rand_obstacle)
            _resultat_creer_obs: tuple[float, bytes] | None = _fn_creer_obstacle(self.__tuiles, self.temps_ecoule())
            #print(_resultat_creer_obs[1])
            #print(_resultat_creer_obs)

            if _resultat_creer_obs is None:
                continue

            _format_paquet_obstacle: bytes = struct.pack(
                paquet.formats_serveur_par_type[TypePaquetServeur.OBSTACLE.value],
                TypePaquetServeur.OBSTACLE.value
            )
            
            _difficulte_atteinte += _resultat_creer_obs[0]
            self.__nouveaux_obstacles.append(_format_paquet_obstacle + _resultat_creer_obs[1])
            #print(self.__tuiles)
        #print(len(self.__nouveaux_obstacles))
        self.__lock = False
        for j in self.__joueurs:
            j.changer_doit_recevoir_maj_obstacles()

        
    @staticmethod
    def __constructeur_obstacle_depuis_type(t: int | TypeObstacle) -> Callable:
        """
        Args:
            t (int | TypeObstacle): Le type d'obstacle
        Returns:
            Le constructeur de ce type d'obstacle

        """
        if isinstance(t, TypeObstacle): t = TypeObstacle.comme_int(t)
        #TODO importer les constructeurs

        match t:
            case TypeObstacle.RIEN.value: return reservation.Reservation.creer
            case TypeObstacle.TRAIN.value: return train.Train.creer
            case TypeObstacle.PILIER.value: return pilier.Pilier.creer
            case TypeObstacle.LASER_CENTRE.value: return laser.Laser.creer
            case TypeObstacle.VAGUE_FEU.value: return vague.Vague.creer
            case TypeObstacle.MISSILE.value:   return missile.Missile.creer

    """
    def __creer_obstacles(self, nouveaux_obstacles: list[TypeObstacle]):
        # TODO Compléter
        for type_o in nouveaux_obstacles:
            self.__nouveaux_obstacles.append()
    """


    def __maj_difficulte(self):
        #self.__difficulte_globale += ModificateurDifficulte.fonction_difficulte(constantes.NIVEAU_DIFFICULTE)(temps_entre_update * 0.1)

        #if math.ceil(self.temps_ecoule()) % 2 == 0:
        if not self.__decider_si_cycle():
            #print(self.__temps_de_jeu)
            Dbg.info("MondeServeur::__maj_difficulte: MAJ Difficulté", 2)

            self.__difficulte_globale = ModificateurDifficulte.fonction_difficulte(self.niveau_difficulte)(self.temps_ecoule())
            #self.__difficulte_globale +=  0.2
            #print(self.__difficulte_globale)


    def nettoyer_tuiles(self):
        for idx_rangee in range(len(self.__tuiles)):
            for idx_t in range(len(self.__tuiles[idx_rangee])):
                if self.__tuiles[idx_rangee][idx_t] is None: continue

                """
                self.__tuiles[idx_rangee][idx_t].duree -= self.__
                
                if self.__tuiles[idx_rangee][idx_t].duree <= 0:
                    self.__tuiles[idx_rangee][idx_t] = None
                """
                if self.__tuiles[idx_rangee][idx_t].mort >= self.temps_ecoule(): # Vérifie si le momemt prévu pour la mort de l'obstacle est déjà passé ou non
                    self.__tuiles[idx_rangee][idx_t] = None
                    Dbg.info("MondeServeur::__nettoyer_tuiles: Nettoyage d'une tuile", 2)



    def temps_ecoule(self) -> float:
        """
        Returns:
            float: Le temps écoulé depuis la création du `MondeServeur.`
        """
        return time.time() - self.__debut

    def __remplacer_moment_maj_anterieure(self, moment: float) -> float:
        self.__moment_maj_anterieure = moment


    def __decider_si_cycle(self) -> bool:
        """
        Considère si assez de temps s'est écoulé (1 seconde) depuis le dernier cycle pour en commencer un autre.
        """
        _t_maintenant: float = self.temps_ecoule()
        Dbg.info(f"MondeServeur::__decider_si_cycle: _t_maintenant = {_t_maintenant}", 5)
        # True si approx(temps écoulé entre le début du jeu et maintenant) et approx(temps écoulé depuis le début du jeu et le dernier cycle) ne sont pas égaux
        # TODO Tester
        _r: bool =  math.ceil(_t_maintenant) != math.ceil(self.__moment_maj_anterieure)
        self.__remplacer_moment_maj_anterieure(_t_maintenant)
        Dbg.info(f"MondeServeur::__decider_si_cycle: Y aura-t-il cycle? : {_r}", 5)

        return _r


    #####################################################################################################
    # FONCTIONS OBSOLÈTES
    #####################################################################################################

    def __obsolète____formatter_dict(self, joueurs_quitte: list[int]):
        """
        Formatte le monde du serveur en json pour l'envoyer au client.
        Style:
            {
                "Général": {
                    "Temps de jeu": <__temps_de_jeu>,
                    "Liste messages": <SignalServeurClient> 
                },

                "Nouveaux Obstacles": [
                    <bytes>
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

        #_fichier_json["Obstacles"]: list[bytes] = []

        _fichier_json["Général"] = {}

        _fichier_json["Général"]["Temps de jeu"] = self.__temps_de_jeu

        _liste_message = []
        for m in self.__liste_messages:

            _liste_message.append(m)

            _fichier_json["Général"]["Liste messages"] = self.__liste_messages


        _fichier_json["Nouveaux obstacles"] = []

        #NOTE Samuel, 12-11-2026: Changement vers l'utilisation des bytes directement pour les obstacles.
        """
        for o in self.__nouveaux_obstacles:

            
            _nouveau_obstacle = {}

            _nouveau_obstacle["Type"] = o.__type_obstacle.value
            _nouveau_obstacle["Position"] = [o.__position[0], o.__position[1], o.__position[2]]

            _fichier_json["Nouveaux obstacles"].append(_nouveau_obstacle)
        """

        #_fichier_json["Obstacles"] = self.__nouveaux_obstacles.copy()
        #self.__nouveaux_obstacles = [] # Remettre à 0

        _fichier_json["Joueurs"] = joueur_abstrait.formatter_json(self.__joueurs)

        _fichier_json["Joueurs quittés"] = joueurs_quitte

        Dbg.info(f"Fichier JSON dabs MondeServeur.__formatter_dict: {_fichier_json}", 3)
        return _fichier_json


    def __obsolète____demarrer_nouvelle_partie(self):
        """
        Commencer une nouvelle partie
        """

        self.__difficulte_globale = 0.0
        self.__temps_de_jeu = 0.0
        self.__partie_en_cours = True
        self.effacer_tout_obstacle()

        Dbg.info("Nouvelle partie commencée", 2)
        self.__liste_message.append("partie_commence")

    def __obsolète____recevoir_creer_id(self, donnee: dict) -> str:
        _temps = time.time()
        for idx, _ in enumerate(self.__joueurs):
            if _temps - _.dernier_paquet > 10:
                self.__joueurs.remove(_)

        if len(self.__joueurs) == 0: self.__derniere_id = 0

        _joueur = JoueurAbstrait()
        _joueur.id = self.__derniere_id

        self.__joueurs.append(_joueur)
        _resultat = json.dumps({'ID': self.__derniere_id})
        Dbg.info(f"[+] Joueur {self.__derniere_id}")
        self.__derniere_id += 1
        return _resultat

    def __obsolète____recevoir_maj(self, donnee: dict) -> str:
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
                Dbg.info(f"[-] Joueur {_joueurs_quittes[0]}")
            else:
                Dbg.info(f"[-] Joueurs {_joueurs_quittes}")

        return json.dumps(self.__formatter_dict(_joueurs_quittes))
        