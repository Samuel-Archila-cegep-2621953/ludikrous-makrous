import tuile
from ursina import Entity


class Monde(Entity):
    def __init__(self, longueur: int, hauteur: int):
        self.__monde: list[list[tuile.Tuile]] = []
        for y in range(hauteur):
            _colonne_tuile = []
            for x in range(longueur):
                _tuile = tuile.Tuile(x, y)
                _colonne_tuile.append(_tuile)
            self.__monde.append(_colonne_tuile)

    def tuile(self, x: int, y: int) -> tuile.Tuile:
        return self.__monde[y][x]

            
