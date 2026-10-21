from enum import Enum

class TypeObstacle(Enum):
    RIEN = 0
    TRAIN = 1
    PILLIER = 2
    LASER_CENTRE = 3
    VAGUE_FEU = 4

    def max(self):
        return 4

