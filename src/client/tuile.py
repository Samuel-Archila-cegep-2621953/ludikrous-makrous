from ursina import *
from ursina.shaders import lit_with_shadows_shader
import config

tuile = load_model('ressources/modeles/tuile.glb')
tuile_texture = load_texture('ressources/textures/plateforme.png')

class Tuile(Entity):
    def __init__(self, x, y):
        super().__init__(model=copy(tuile), texture=tuile_texture, color=rgb(128/255,128/255,128/255), rotation=(-90, 0, 0), position=(x*5,-5,y*5), scale=(0.5, 0.5, 0.5), collider='box')
