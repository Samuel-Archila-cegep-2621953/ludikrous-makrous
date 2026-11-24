import tuile
from ursina import *
import time

dehors = load_model('ressources/modeles/data_center_final_question_mark.glb')

class Monde:
    def __init__(self, longueur: int, hauteur: int):
        self.debut = time.time()
        self.__monde: list[list[tuile.Tuile]] = []
        self.__ext = Entity(model=copy(dehors), position=(17.5, 0, 17.5), scale=(4,4,4), rotation=(-90,90,0))
    
        for y in range(hauteur):
            _colonne_tuile = []
            for x in range(longueur):
                _tuile = tuile.Tuile(x, y, self.debut)
                _tuile.visible_setter(False)
                _colonne_tuile.append(_tuile)
            self.__monde.append(_colonne_tuile)

    def changer_visibilite(self):
        for rang in self.__monde:
            for tuile in rang:
                tuile.visible_setter(True)

    def tuile(self, x: int, y: int) -> tuile.Tuile:
        return self.__monde[y][x]

    def changer_hauteur_tuile(self, x: int, y: int, h: float):
        self.tuile(x, y).changer_hauteur(h, time.time())