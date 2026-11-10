from obstacle import Obstacle
from type_obstacle import TypeObstacle
from coord import Coord
import random

class Pilier(Obstacle):
    def __init__(self, coord: Coord):
        super().__init__()
        self.difficulte: float = 0.1 * coord.z
        self.__type_obstacle = TypeObstacle.PILIER
        self.__position: Coord = coord
        self.duree: float = random.uniform(1, 15) 
        self.est_global = False
        self.transparent = False

    

    