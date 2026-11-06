from enum import Enum
import struct

class TypeObstacle(Enum):
    RIEN = 0
    TRAIN = 1
    PILIER = 2
    LASER_CENTRE = 3
    VAGUE_FEU = 4

    @staticmethod
    def max():
        return 4


    @staticmethod
    def comme_int(type_obstacle: 'TypeObstacle') -> int:
        return type_obstacle.value

    @staticmethod
    def depuis_int(n: int) -> 'TypeObstacle':
        match n:
            case TypeObstacle.RIEN.value:      return TypeObstacle.RIEN
            case TypeObstacle.TRAIN.value:      return TypeObstacle.TRAIN
            case TypeObstacle.PILIER.value:      return TypeObstacle.PILIER
            case TypeObstacle.LASER_CENTRE.value: return TypeObstacle.LASER_CENTRE
            case TypeObstacle.VAGUE_FEU.value:     return TypeObstacle.VAGUE_FEU

    @staticmethod
    def format(type_obstacle: 'int | TypeObstacle') -> str:
        if isinstance(type_obstacle, TypeObstacle):
            type_obstacle = TypeObstacle.comme_int(type_obstacle)

        _formats = [
            None,
            'B B BB', #type obstacle, NB COORDONNEES, Coord initiale, liste de coordonnees
            'B BB f', # Type obs, coord, hauteur
            'B BB f', # Type obs, coord, rayon
            'B B f', # Type obs, direction, hauteur
        ]
        return _formats[type_obstacle]


    def nb_bytes(t: int) -> int:
        """
        Calcule le nombre d'octets à lire selon le type d'obstacle
        """
        return struct.calcsize('!' + TypeObstacle.format(t))


    @staticmethod
    def dict_depuis_tuple(donnees: tuple['int | TypeObstacle', tuple[any]]) -> dict[str, any]:
        _type: int = donnees[0]
        match _type:
            case TypeObstacle.VAGUE_FEU.value: 
                _, direction, hauteur = donnees[1]
                return {
                    "Type": _type,
                    "Direction": direction,
                    "Hauteur": hauteur
                }

            case TypeObstacle.LASER_CENTRE.value:
                _, x, y, r = donnees[1]
                return {
                    "Type": _type,
                    "Coord": (x, y),
                    "Rayon": r
                }

            case TypeObstacle.PILIER.value:
                _, x, y, h = donnees[1]
                return {
                    "Type": _type,
                    "Coord": (x, y),
                    "Hauteur": h
                }

            case TypeObstacle.TRAIN.value:
                pass #TODO

