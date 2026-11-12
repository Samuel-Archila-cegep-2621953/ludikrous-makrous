from obstacle import Obstacle
from type_obstacle import TypeObstacle
from coord import Coord
import random
import struct
from tuile import Tuile

class Pilier(Obstacle):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.mode_hauteur: int = random.randint(1, 5)
        self.difficulte: float = 0.1 * self.mode_hauteur
        self.__type_obstacle = TypeObstacle.PILIER
        self.position: tuple[int, int] = (x, y)
        #self.duree: float = random.uniform(1, 15) 
        self.duree: int = 7
        self.est_global = False
        self.transparent = False


    @staticmethod
    def creer(monde: list[list[Tuile]]) -> tuple[float, bytes] | None:
        """
        Args:
            monde (`&list[list[Tuile]]`): Le mond du serveur. Permet de vérifier s'il existe une position adéquate pour l'obstacle.
        Returns:
            `bytes`: L'obstacle comme paquet, en `bytes`  
            `float`: La difficultà de cet obstacle
            `None`: Si il n'est pas possible de placer cet obstacle nulle part
        """
        #print(monde)
        for y, rangees in enumerate(monde):
            for x, t in enumerate(rangees):
                if t is None: #NOTE None -> La tuile n'a aucun obstacle
                    monde[y][x] = Pilier(x, y)
                    return (monde[y][x].difficulte, monde[y][x].comme_bytes())


    def comme_bytes(self) -> bytes:
        _format: str = TypeObstacle.format(self.__type_obstacle.value)
        #print(f"format {_format}")
        return struct.pack(
            _format,
            self.__type_obstacle.value,
            self.position[0],
            self.position[1],
            self.mode_hauteur
        )