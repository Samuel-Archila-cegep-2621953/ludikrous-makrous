from ursina.prefabs.first_person_controller import FirstPersonController
import client_serveur
import time
import json
import joueur
from ursina import *

class JoueurClient(FirstPersonController):
    def __init__(self, client: client_serveur.Client, height=2, **kwargs):
        super().__init__(height, **kwargs)
        self.__client = client
        self.__dernier_temps = self.__obtenir_temps()
        self.__joueurs: list[joueur.Joueur] = []

    def __obtenir_temps(self) -> float:
        return time.time()

    def __emballer_les_donnees(self) -> str:
        return json.dumps({
            "Position": [
                self.position.x,
                self.position.y,
                self.position.z
            ]
        })

    def joueurs(self) -> list[joueur.Joueur]:
        return self.__joueurs

    def lire_donnee(self, donnee_texte: str):
        print(len(self.__joueurs))
        _donnee = json.loads(donnee_texte)

        _joueurs = _donnee["Joueurs"]
        for i, _ in enumerate(_joueurs):
            _position = _['Position']
            if i >= len(self.__joueurs):
                self.__joueurs.append(joueur.Joueur(i, '', (_position[0], _position[1], _position[2]), model='cube', color=rgb(255,0,0), scale=1))
            else:
                self.__joueurs[i].position = (_position[0], _position[1], _position[2])


    def update(self):
        super().update()
        temps_en_ce_moment = self.__obtenir_temps()
        if temps_en_ce_moment - self.__dernier_temps > 1 / 12:
            self.lire_donnee(self.__client.envoyer_message(self.__emballer_les_donnees()))