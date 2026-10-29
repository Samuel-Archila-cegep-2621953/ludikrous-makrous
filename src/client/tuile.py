from ursina import *
from ursina.shaders import lit_with_shadows_shader 

class Tuile(Entity):
    def __init__(self, x, y):
        super().__init__(model='cube', color=rgb(128/255,128/255,128/255), scale=(10,1,10), position=(x*11,-2,y*11),collider='box', shader=lit_with_shadows_shader)
