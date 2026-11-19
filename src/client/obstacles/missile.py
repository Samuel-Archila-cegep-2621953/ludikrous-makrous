from ursina import *

class Missile:
    class Missile_Object(Entity):
        def __init__(self, position, supprimer, joueur):
            super().__init__(model='cube', position=position)
            self.__supprimer = supprimer
            self.__joueur = joueur
        def update(self):
            import joueur_client
            self.y -= 40 * time.dt
            # logique
            ray = raycast(self.world_position, self.down)
            if ray.distance < 0.3:
                _dist = (self.position.x - self.__joueur.position.x)**2 + (self.position.y - self.__joueur.position.y)**2 + (self.position.z - self.__joueur.position.z)**2
                self.__joueur.vie.value -= int(clamp((20 - _dist) * 15, 0, 200))
                self.__supprimer()

    def __init__(self, position: tuple[int,int], joueur):
        """
        Args:
            position (tuple[int,int]): position X et Y relatif au tuiles
        """
        self.__position = position

        self.__cible = Entity(model='cube', scale=(1, 20, 1), position=(self.__position[0] * 4, 0, self.__position[1] * 4))
        self.__missile = None
        self.__joueur = joueur

        invoke(self.__apparaitre_missile, delay=2)

    def __apparaitre_missile(self):
        self.__cible.visible_setter(False)
        self.__missile = self.Missile_Object((self.__position[0] * 4, 20, self.__position[1] * 4), self.__supprimer, self.__joueur)

    def __supprimer(self):
        destroy(self.__cible)
        if self.__missile is not None:
            destroy(self.__missile)
        del self