from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu
from musique import Musique

class Menu(Entity):
    def __init__(
            self, 
            nom: str,
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
            nom (str): Le nom du menu
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
        self.nom = nom

        #print(str(type(boutons)))

        for x in boutons + autres + textes + menus_deroulants:
            x.parent = self.menu
            x.enabled = enabled

        self.boutons = boutons
        self.textes = textes
        self.menus_deroulants = menus_deroulants
        self.autres = autres


    def jouer_musique(self):
        if self.musique is not None:
            self.musique.play()


    def play(self):
        """Alias pour Menu.joueur_musique()"""
        self.jouer_musique()


    def arreter_musique(self):
        if self.musique is not None:
            self.musique.stop()


    def stop(self):
        """Alias pour Menu.arreter_musique()"""
        self.arreter_musique()
    

    def montrer(self):
        """
        Active le `Menu`
        """
        self.menu.enable()
        self.fond.enable()
        #for b in self.boutons:
         #   b.text_entity.text = b.text
        for x in self.boutons + self.autres + self.textes + self.menus_deroulants:
            x.enabled = True
        self.jouer_musique()
            

    def cacher(self):
        """
        Désactive le `Menu`
        """
        self.menu.disable()
        for x in self.boutons + self.autres + self.textes + self.menus_deroulants:
            self.enabled = False
        self.musique.fade_out(0.5)


    def disable(self):
        """
        Alias de `Menu.cacher()`
        """
        self.cacher()


    def enable(self):
        """
        Alias de `Menu.montrer()`
        """
        self.montrer()

        
        

