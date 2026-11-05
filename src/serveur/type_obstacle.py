from enum import Enum

class TypeObstacle(Enum):
    RIEN = 0
    TRAIN = 1
    PILIER = 2
    LASER_CENTRE = 3
    VAGUE_FEU = 4

    @staticmethod
    def max():
        return 4


    def comme_int(type_obstacle: 'TypeObstacle') -> int:
        match type_obstacle:
            case TypeObstacle.RIEN:         return 0
            case TypeObstacle.TRAIN:        return 1
            case TypeObstacle.PILIER:       return 2
            case TypeObstacle.LASER_CENTRE: return 3
            case TypeObstacle.VAGUE_FEU:    return 4


    @staticmethod
    def format(type_obstacle: 'int | TypeObstacle') -> str:
        if isinstance(type_obstacle, TypeObstacle):
            type_obstacle = TypeObstacle.comme_int(type_obstacle)

        _formats = [
            '',
            'B BB B(B...)', #Format, COORD, initiale, NB COORDONNEES, liste de coordonnees
            'B BB f', # Type, coord, hauteur
            'B BB f', # Type, coord, rayon
            'B B f', # Type, direction, hauteur
        ]
        return _formats[type_obstacle]


