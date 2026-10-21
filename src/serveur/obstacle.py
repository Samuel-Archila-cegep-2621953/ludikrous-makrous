from type_obstacle import TypeObstacle

class Obstacle:
    def __init__(self, arg):

        self.__position = (0, 0)
        self.__temps_en_vie = 0 #le temps en vie détermine son comportement, comme pour le train
        self.__type_obstacle = TypeObstacle.RIEN
        self.difficulte = None # La difficulté de l'obstacle seul

    def position(self) -> tuple[float,float]:
        return self.__position

    def temps_en_vie(self) -> int:
        return self.__temps_en_vie

    def type_obstacle(self) -> int:
        return self.__type_obstacle

    def mise_a_jour(self, temps) -> float:
        __temps_en_vie += temps

    def creer(self):
        pass

    def detruire(self):
        pass

