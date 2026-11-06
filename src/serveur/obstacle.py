from type_obstacle import TypeObstacle
from abc import ABC, abstractmethod

class Obstacle:
    def __init__(self, arg):

        self.__temps_en_vie = 0 #Combien de temps cet obstacle a éxisté
        self.__type_obstacle = TypeObstacle.RIEN
        self.difficulte = None # La difficulté de l'obstacle seul
        self.duree = None # La duree de vie de l'obstacle en secondes
        self.__position = None
        self.est_global = None # Détermine si cet obstacle est nécessairement lié à une case spécifique
        self.transparent = None # Détermine si un autre obstacle peut passe à travers de cet obstacle

    def position(self) -> tuple[float,float]:
        return self.__position

    def temps_en_vie(self) -> int:
        return self.__temps_en_vie

    def type_obstacle(self) -> TypeObstacle:
        return self.__type_obstacle

    def mise_a_jour(self, temps) -> float:
        self.__temps_en_vie += temps

    @abstractmethod
    def creer(self) -> bytes:
        pass

    def detruire(self):
        pass


    #def 