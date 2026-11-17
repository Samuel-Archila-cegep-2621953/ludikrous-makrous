
from obstacle import Obstacle
from type_obstacle import TypeObstacle
from coord import Coord
import random
from tuile import Tuile

class Reservation(Obstacle):
    # Permet de bloquer la création d'un obstacle sur une tuile
    def __init__(self, x: int, y: int, moment: float):
        self.z = 0
        self.__type_obstacle = TypeObstacle.RIEN
        self.difficulte = 0 # La difficulté de l'obstacle seul
        self.duree = 17 # La duree de vie de l'obstacle en secondes
        self.x = x
        self.y = y
        self.est_global = False
        self.mort = self.determiner_mort(moment)
        self.transparent = True


    def creer(monde: list[list[Tuile]], naissance: float) -> None:
        for _ in range(8):
            _posx = random.randint(0, 7)
            _posy = random.randint(0, 7)
            if monde[_posy][_posx] is None:
                monde[_posy][_posx] = Reservation(_posx, _posy, naissance)

        return None

    def determiner_mort(self, naissance: float):
        return naissance + self.duree