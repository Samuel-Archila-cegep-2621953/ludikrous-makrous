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
            roundness=0.3, 
            value=255, 
            max_value=255, 
            y=0.45, 
            x= -0.8, 
            color=rgb(129/255,129/255,129/255), 
            scale=(0.3, 0.05)
        )
        self.cursor.visible = False

        _chemin_musique = Musique.aleatoire(TypesMusique.JEU_FACILE)
        self.musique = Audio(_chemin_musique, loop=True, volume=0.7)
        self.__chemin_musique = _chemin_musique

    def __creer_id(self) -> int:
        _resultat = self.__client.envoyer_message(json.dumps({
                "Type": "CREER ID"
            }))
        _donnee = json.loads(_resultat)
        return _donnee['ID']

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
            self.lire_donnee(self.__client.envoyer_message(self.__emballer_les_donnees()))
        
        #print(self.position)
        if self.position.y < -10:
            self.position = (60, 0, 60)

        if self.position.x > 72 and self.position.z > 72 and self.__chemin_musique != "ressources/sons/musique/jeu/victoire/mi_corazoncito.ogg":
            print(self.__chemin_musique)
            self.__chemin_musique = Musique.aleatoire(TypesMusique.VICTOIRE)
            self.musique.fade_out(duration=0.3)
            self.musique = Audio(self.__chemin_musique, loop=True, volume=0.7).fade_in(duration=0.7)

    def input(self,key):
        super().input(key)
        match key:
            case "escape": principale.terminer_jeu()
            case "-": self.vie.value -= 10
            case "=": self.vie.value += 10