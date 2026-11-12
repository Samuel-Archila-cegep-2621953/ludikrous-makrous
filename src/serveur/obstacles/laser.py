
from obstacle import Obstacle
from type_obstacle import TypeObstacle
from coord import Coord
import random

class Laser(Obstacle):
    def __init__(self, coord: Coord):
        coord.z = 0
        self.__type_obstacle = TypeObstacle.LASER_CENTRE
        self.__longueur: float = random.uniform(0.1, 1) # TODO Définir la longueur max comme la moitié de la longueur d'un coté d'une case
        self.difficulte = 0.12 * self.__longueur # La difficulté de l'obstacle seul
        self.duree = 10 # La duree de vie de l'obstacle en secondes
        self.__position = coord
        self.est_global = False
        self.transparent = False

    def creer(self) -> bytes:
        pass