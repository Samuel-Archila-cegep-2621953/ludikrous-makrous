from ursina import *

missile = load_model('ressources/modeles/missile.glb')

class Missile:
    class Missile_Objet(Entity):
        def __init__(self, position, supprimer, joueur):
            super().__init__(model=copy(missile), position=position, rotation=(-90, 0, 0), scale=(0.5,0.5,0.5))
            self.__supprimer = supprimer
            self.__joueur = joueur
            self.__col = False
            self.__expl = None
        def update(self):
            if self.__col: return
            import joueur_client
            self.y -= 40 * time.dt
            # logique
            ray = raycast(self.world_position + (0,1,0), self.down)
            if ray.distance < 5:
                _dist = (self.position.x - self.__joueur.position.x)**2 + (self.position.y - self.__joueur.position.y)**2 + (self.position.z - self.__joueur.position.z)**2
                self.__joueur.vie.value -= int(clamp((40 - _dist) * 15, 0, 200))
                self.__col = True
                self.visible_setter(False)
                self.__expl = Entity(model='sphere', scale=(6.5,6.5,6.5), position=self.position, color=color.orange)
                self.__expl.alpha_setter(0.7)
                self.__expl.fade_out(0, 0.3)
                invoke(self.__supprimer_explosion, delay=0.3)
                invoke(self.__supprimer, delay=2)
        def __supprimer_explosion(self):
            destroy(self.__expl)

    def __init__(self, position: tuple[int,int], joueur):
        """
        Args:
            position (tuple[int,int]): position X et Y relatif au tuiles
        """
        self.__position = position

        self.__cible = Entity(model='cube', scale=(1, 100, 1), position=(self.__position[0] * 5, 5, self.__position[1] * 5))
        self.__missile = None
        self.__joueur = joueur

        self.__cible.fade_out(0, duration= 0.5)

        invoke(self.__apparaitre_missile, delay=0.5)

    def __apparaitre_missile(self):
        #self.__cible.visible_setter(False)
        self.__missile = self.Missile_Objet((self.__position[0] * 5, 20, self.__position[1] * 5), self.__supprimer, self.__joueur)

    def __supprimer(self):
        destroy(self.__cible)
        if self.__missile is not None:
            destroy(self.__missile)
        del self