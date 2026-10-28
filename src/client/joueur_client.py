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
import type_paquet
from config import Config

class JoueurClient(FirstPersonController):
    def __init__(self, client: client_serveur.Client, height=2, **kwargs):
        super().__init__(height, **kwargs)
        self.__client = client
        self.__id = self.__creer_id()
        #print(self.__id)
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

        _mdp_hache = Config.json()["Client"]["mot_de_passe_hache"].encode("utf-8")
        _nom_utilisateur = Config.json()["Client"]["nom_utilisateur"].encode("utf-8")

        _resultat = self.__client.envoyer_message(struct.pack(type_paquet.formats_clients_par_type[1], 1, _nom_utilisateur, _mdp_hache))
        #return _donnee['ID']
        return 6

    def __obtenir_temps(self) -> float:
        return time.time()

    def __emballer_les_donnees(self) -> str:
        return json.dumps({
            "Type": "MAJ",
            "ID": self.__id,
            "Position": [
                self.position.x,
                self.position.y,
                self.position.z
            ]
        })

    def joueurs(self) -> list[joueur.Joueur]:
        return self.__joueurs

    def lire_donnee(self, donnee_texte: str):
        _donnee = json.loads(donnee_texte)

        _joueurs = _donnee["Joueurs"]
        for i, _ in enumerate(_joueurs):
            _position = _['Position']
            if i >= len(self.__joueurs):
                _joueur = joueur.Joueur(_joueurs[i]["ID"], '', (_position[0], _position[1], _position[2]))
                self.__joueurs.append(_joueur)
            else:
                self.__joueurs[i].position = (_position[0], _position[1] + 1.25, _position[2])
        for _ in _donnee['Joueurs quittés']:
            destroy(self.__joueurs[_])
            del self.__joueurs[_]


    def update(self):
        super().update()
        temps_en_ce_moment = self.__obtenir_temps()
        if temps_en_ce_moment - self.__dernier_temps > 1 / 12:
            self.lire_donnee(Pq.interpreter_paquet(self.__client.envoyer_message(self.__emballer_les_donnees())))
        
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