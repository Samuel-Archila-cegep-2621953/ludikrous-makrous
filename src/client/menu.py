from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu
from musique import Musique

class Menu(Entity):
    def __init__(
            self, 
            texture_fond, 
            musique: Musique = None, 
            boutons: list[Button] = [], 
            textes: list[Text] = [],
            menus_deroulants: list[DropdownMenu] = []
        ):
        """
        Un menu. Les parents sont automatiquement définis comme le fond.
        Args:
            texture_fond (str ou ursina.Texture): La texture du fond du menu. Inclue déjà `ressources/textures/`
            musique (Musique): La musique à joueur dans ce menu
            boutons (list[ursina.Button]): La liste de boutons
            textes (list[Text]): Une liste contenant le ou les textes à afficher
            menus_deroulants: list[ursina.prefabs.dropdown_menu.DropdownMenu]: Une liste contenant le ou les menus déroulants
        """
        self.fond = Entity(parent = camera.ui, model = 'quad', scale = (window.aspect_ratio, 1), texture = f"ressources/textures/{texture_fond}", enabled = False)
        self.musique = musique

        for b in boutons:
            b.parent = self.fond
        self.boutons = boutons
        self.textes = textes
        self.menus_deroulants = menus_deroulants


    def montrer(self):
        """
        Active le `Menu`
        """
        self.fond.enable()
