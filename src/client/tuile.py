from ursina import *
from ursina.shaders import lit_with_shadows_shader
import random

tuile = load_model('ressources/modeles/tuile.glb')
tuile_texture = load_texture('ressources/textures/plateforme.png')

class Tuile(Entity):
    def __init__(self, x, y):
        h = random.uniform(-7, -3)
        H_DEFAUT: float = -5
        super().__init__(
            model=copy(tuile), 
            texture=tuile_texture, 
            color=rgb(128/255,128/255,128/255), 
            rotation=(-90, 0, 0), 
            position=(x*5, H_DEFAUT,y*5), 
            scale=(0.5, 0.5, 0.5), 
            collider='box'
        )
        self.doit_y = self.y
        self.vitesse = 1

    def __similaire(self, y1, y2, maximum):
        return abs(y1 - y2) < maximum

    def update(self):
        _direction = 1 if self.y < self.doit_y else -1
        if self.__similaire(self.y, self.doit_y, 0.3):
            self.y = self.doit_y
        else:
            self.y += self.vitesse * time.dt * _direction

    def changer_hauteur(self, h: float):
        self.doit_y = h


