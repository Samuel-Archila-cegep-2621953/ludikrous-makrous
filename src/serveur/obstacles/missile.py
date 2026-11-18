
from obstacle import Obstacle
from type_obstacle import TypeObstacle
from coord import Coord
import random
from tuile import Tuile
import struct

class Missile(Obstacle):
    def __init__(self, x: int, y: int, moment_creation: float):
        self.__type_obstacle = TypeObstacle.MISSILE
        self.__longueur: float = random.uniform(0.1, 1) # TODO Définir la longueur max comme la moitié de la longueur d'un coté d'une case
        self.difficulte = 3 # La difficulté de l'obstacle seul
        self.duree = 5 # La duree de vie de l'obstacle en secondes
        self.position: tuple[int, int] = (x, y)
        self.est_global = False
        self.transparent = False
        self.mort: float = self.determiner_mort(moment_creation)

    @staticmethod
    def creer(monde: list[list[Tuile]], naissance: float) -> tuple[float, bytes] | None: 
        _chance = random.randint(0,1)
        if _chance == 0: return None
        for _ in range(8):
            _x = random.randint(0, 7)
            _y = random.randint(0, 7)
            if monde[_y][_x] is None:
                monde[_y][_x] = Missile(_x, _y, naissance)
                return (monde[_y][_x].difficulte, monde[_y][_x].comme_bytes()) 
        return None

    def determiner_mort(self, en_ce_moment: float):
        return en_ce_moment + self.duree

    def comme_bytes(self) -> bytes:
        _format: str = TypeObstacle.format(self.__type_obstacle.value)
        return struct.pack(
            _format,
            self.__type_obstacle.value,
            self.position[0],
            self.position[1]
        )