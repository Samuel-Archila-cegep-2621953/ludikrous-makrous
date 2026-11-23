from ursina import *
from ursina.shaders import lit_with_shadows_shader
import random
from pilier import Pilier
import time
from debogage import Debogage as Dbg

tuile = load_model('ressources/modeles/tuile.glb')

class Tuile(Entity):
    H_DEFAUT: float = -5
    def __init__(self, x, y, moment_creation: float):
        h = random.uniform(-7, -3)
        super().__init__(
            model=copy(tuile),
            color=color.dark_gray,
            rotation=(-90, 0, 0), 
            position=(x*5, Tuile.H_DEFAUT,y*5), 
            scale=(0.5, 0.5, 0.5), 
            collider='box'
        )
        self.doit_y = self.y
        self.vitesse = 5
        self.creation = moment_creation
        self.dernier_var_h = 0
        self.prochaine_mort = None

    def __similaire(self, y1, y2, maximum):
        return abs(y1 - y2) < maximum

    def update(self):
        _direction = 1 if self.y < self.doit_y else -1
        if self.__similaire(self.y, self.doit_y, 0.3):
            self.y = self.doit_y
        else:
            _multiplicateur = 2 if self.doit_y < -10 else 1
            self.y += self.vitesse * time.dt * _direction * _multiplicateur
        self.visible_setter(self.y > -10)

        if self.prochaine_mort is not None and time.time() >= self.prochaine_mort:
            self.doit_y = Tuile.H_DEFAUT
            self.prochaine_mort = None
            Dbg.info("Tuile::update: Retour vers hauteur par défaut", 3)

        

    def changer_hauteur(self, h: float, t: float):
        self.doit_y = h
        self.prochaine_mort = t + Pilier.DUREE


