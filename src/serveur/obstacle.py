from type_obstacle import TypeObstacle
from abc import ABC, abstractmethod
from tuile import Tuile

class Obstacle:
    def __init__(self):

        self.__temps_en_vie = 0 #Combien de temps cet obstacle a éxisté
        self.__type_obstacle = TypeObstacle.RIEN
        self.difficulte = None # La difficulté de l'obstacle seul
        self.duree = None # La duree de vie de l'obstacle en secondes
        self.__position = None
        self.est_global = None # Détermine si cet obstacle est nécessairement lié à une case spécifique
        self.transparent = None # Détermine si un autre obstacle peut passe à travers de cet obstacle
        self.naissance: float = None # Le moment ou l'obstacle a été créé

    def temps_en_vie(self) -> int:
        return self.__temps_en_vie

    def type_obstacle(self) -> TypeObstacle:
        return self.__type_obstacle

    @abstractmethod
    def creer(monde: list[list[Tuile]]) -> tuple[float, bytes] | None:
        pass

    def detruire(self):
        pass

    @abstractmethod
    def determiner_mort(self) -> float:
        pass
