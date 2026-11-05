
from obstacle import Obstacle
from type_obstacle import TypeObstacle
from coord import Coord
import random

class Train(Obstacle):
    def __init__(self, origine: Coord):
        super().__init__()
        self.difficulte: float = None
        self.__type_obstacle = TypeObstacle.PILIER
        self.__position: Coord = None
        self.est_global = True


    def __calculer_difficulte(self) -> float:
        pass


    def calculer_duree() -> float:
        pass