from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu
from musique import Musique

class Menu(Entity):
    def __init__(
            self, 
            texture_fond, 
            musique: Musique = None, 
            boutons: list[Button] = [], 
            autres: list[Entity] = [],
            textes: list[Text] = [],
            menus_deroulants: list[DropdownMenu] = [],
            enabled = True
        ):
        """
        Un menu. Les parents sont automatiquement définis comme le fond.
        Args:
            texture_fond (str ou ursina.Texture): La texture du fond du menu. Inclue déjà `ressources/textures/`
            musique (Musique): La musique à joueur dans ce menu
            boutons (list[ursina.Button]): La liste de boutons
            autres (list[ursina.Entity]): Une liste d'autres `Entity`. Par exemple, pour le logo du jeu dans le menu principal
            textes (list[Text]): Une liste contenant le ou les textes à afficher
            menus_deroulants: list[ursina.prefabs.dropdown_menu.DropdownMenu]: Une liste contenant le ou les menus déroulants
        """
        super().__init__()
        self.menu = Entity(parent = camera.ui)
        self.fond = Entity(parent = self.menu, model = 'quad', scale = (window.aspect_ratio, 1), texture = f"ressources/textures/{texture_fond}", enabled = enabled, z=1)
        self.musique = musique

        for b in boutons + autres + textes + menus_deroulants:
            b.parent = self.menu

        self.boutons = boutons
        self.textes = textes
        self.menus_deroulants = menus_deroulants


    def montrer(self):
        """
        Active le `Menu`
        """
        self.menu.enable()
        self.musique.play()
            

    def cacher(self):
        """
        Désactive le `Menu`
        """
        self.menu.disable()
        self.musique.fade_out(0.5)

