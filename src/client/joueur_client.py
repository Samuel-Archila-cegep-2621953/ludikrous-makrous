from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
import client_serveur
import time
import json
import joueur
from ursina import *
import __main__ as principale
from types_musique import TypesMusique
from musique import Musique
import paquet as Pq
import struct
from type_paquet import *
from config import Config
from math import isnan as is_nan

class JoueurClient(FirstPersonController):
    def __init__(self, client: client_serveur.Client, height=2, **kwargs):
        super().__init__(height, **kwargs)
        self.__client = client
        self.__id = self.__creer_id()
        self.__dernier_temps = self.__obtenir_temps()
        self.__joueurs: list[joueur.Joueur] = []
        self.vie = HealthBar(
            parent=camera.ui, 
            bar_color=rgb(84/255, 23/255, 14/255), 
            roundness=0, 
            value=255, 
            max_value=255, 
            y=0.45, 
            x= -0.8, 
            color=rgb(129/255,129/255,129/255), 
            scale=(0.3, 0.05),
            show_text=False
        )
        self.cursor.visible = False

        self.musique = Musique(TypesMusique.PERTE)
        self.musique.fade_in(0.7)

    def __creer_id(self) -> int:
        """
        _resultat = self.__client.envoyer_message(json.dumps({
                "Type": "CREER ID"
            }))
        _donnee = json.loads(_resultat)
        """

        #_mdp_hache = Config.json()["Client"]["mot_de_passe_hache"].encode("ascii")
        _mdp_hache = bytes.fromhex(Config.json()["Client"]["mot_de_passe_hache"].strip())
        _nom_utilisateur = Config.json()["Client"]["nom_utilisateur"].encode("ascii")
        print(_mdp_hache)

        _hache = self.__client.envoyer_message(struct.pack(
            formats_clients_par_type[TypePaquetClient.CONNEXION.value],
            TypePaquetClient.CONNEXION.value, 
            _nom_utilisateur, 
            _mdp_hache)
        )["Connexion"]

        print(f"[+] Hache obtenue: {_hache}")
        #return _donnee['ID']
        if _hache == None: exit(1)
        return _hache

    def __obtenir_temps(self) -> float:
        return time.time()

    def __emballer_les_donnees(self) -> bytes:
        """
        return json.dumps({
            "Type": "MAJ",
            "ID": self.__id,
            "Position": [
                self.position.x,
                self.position.y,
                self.position.z
            ]
        })
        """
        #TODO! Convertir en struct
        return struct.pack(
                formats_clients_par_type[TypePaquetClient.MAJ_JOUEUR.value], # FORMAT
                #NOTE VIEUX TypePaquetClient.MAJ_JOUEUR.value[0],
                TypePaquetClient.MAJ_JOUEUR.value,                            # TYPE
                #NOTE VIEUX Config.json()["Client"]["mot_de_passe_hache"].encode("ascii"),
                self.__id, # hache clé
                floor(self.position.x * 100),
                floor(self.position.y * 100),
                floor(self.position.z * 100),
                self.vie.value,
                3 # TODO Animations
            )

    def joueurs(self) -> list[joueur.Joueur]:
        return self.__joueurs

    def lire_donnee(self, donnee_texte: dict):
        #NOTE VEUX_donnee = json.loads(donnee_texte)
        _donnee = donnee_texte
        print("DONNEES LUES")

        _joueurs = _donnee["Joueurs"]
        for i, _ in enumerate(_joueurs):
            _position: list[float] = _['Position']

            for p_idx, p in enumerate(_position):
                if is_nan(p):
                    print(f"ERREUR0: Position d'un joueur est NaN. Position: {_position}")
                    _position[p_idx] = 0.0

            if i >= len(self.__joueurs):
                _joueur = joueur.Joueur(_joueurs[i]["ID"], '', (_position[0], _position[1], _position[2]))
                self.__joueurs.append(_joueur)
            
            #else:
            elif _["ID"] != self.__id:  # Ne pas se mettre à jour soi-même?
                _pos = (_position[0] / 100, _position[1] + 1.25, _position[2] / 100)
                print(_pos)
                for p_idx, p in enumerate(_pos):
                    if is_nan(p):
                        print(f"ERREUR1: Position d'un joueur est NaN. Position: {_position}")
                        _position[p_idx] = 0.0
                        print(f"Position corrigée: {_pos}")
                self.__joueurs[i].position = _pos
        
        for jq in _donnee['Joueurs quittés']:
            destroy(self.__joueurs[jq])
            del self.__joueurs[jq]

        _obstacles = _donnee["Obstacles"]
        #for j, obs in enumerate(_obstacles):



    def update(self):
        super().update()
        temps_en_ce_moment = self.__obtenir_temps()
        if temps_en_ce_moment - self.__dernier_temps > 1 / 12:
            #NOTE VIEUX self.lire_donnee(Pq.interpreter_paquet(self.__client.envoyer_message(self.__emballer_les_donnees())), TypePaquetServeur.MAJ_JOUEUR)
            self.lire_donnee(self.__client.envoyer_message(self.__emballer_les_donnees()))
        
        #print(self.position)
        if self.position.y < -10:
            self.position = (60, 0, 60)


    def reduire_vie(self, quantite: float):
        self.vie.value -= quantite

        
    def input(self,key):
        super().input(key)
        match key:
            case "escape": principale.terminer_jeu()
            case "-": self.reduire_vie(3)
            case "=": self.vie.value += 10


    def creer_liste_score():
        """
        Reçoit une liste de joueurs des serveurs et crée une list[tuple[str, int]] contenant les noms et scores des joueurs
        """
        # TODO!
        pass