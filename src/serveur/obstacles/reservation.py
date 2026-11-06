
from obstacle import Obstacle
from type_obstacle import TypeObstacle
from coord import Coord
import random

class Reservation(Obstacle):
    # Permet de bloquer la création d'un obstacle sur une tuile
    def __init__(self, coord: Coord):
        coord.z = 0
        self.__type_obstacle = TypeObstacle.RIEN
        self.difficulte = 0 # La difficulté de l'obstacle seul
        self.duree = 45 # La duree de vie de l'obstacle en secondes
        self.__position = coord
        self.est_global = False
        self.transparent = True