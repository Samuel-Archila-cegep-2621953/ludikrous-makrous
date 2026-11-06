from obstacle import Obstacle
from type_obstacle import TypeObstacle
from coord import Coord
import random

class Vague(Obstacle):
    def __init__(self, coord: Coord):
        self.__type_obstacle = TypeObstacle.VAGUE_FEU
        self.difficulte = 0.5 # La difficulté de l'obstacle seul
        self.duree = 1 # La duree de vie de l'obstacle en secondes
        self.__position = coord
        self.est_global = True
        self.transparent = True
