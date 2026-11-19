from ursina import *

class Missile:
    def __init__(self, position: tuple[int,int]):
        """
        Args:
            position (tuple[int,int]): position X et Y relatif au tuiles
        """
        self.__position = position

        self.__cible = Entity(model='cube', scale=(1, 20, 1), position=(self.__position[0] * 4, 0, self.__position[1] * 4))
        self.__missile = None

        invoke(self.__apparaitre_missile, delay=2)

    def __apparaitre_missile(self):
        self.__cible.visible_setter(False)
        self.__missile = Entity(model='cube', scale=(1,1,1), position=(self.__position[0] * 4, 20, self.__position[1] * 4))

    def __del__(self):
        destroy(self.__cible)
        if self.__missile is not None:
            destroy(self.__missile)