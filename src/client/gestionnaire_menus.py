from menu import Menu
from array import array
from ursina import *

# Peut-être ça sera utilisé

class GestionnaireMenus:
    liste: list[Menu] = [None, None, None]

    def ajouter(prochain: Menu):
        """
        Ajoute le prochain menu après la fin de celui qui est activé en ce moment
        Args: 
            prochain (Menu): Le prochain menu à montrer

        """
        GestionnaireMenus.liste[0] = GestionnaireMenus.liste[1]
        GestionnaireMenus.liste[1] = prochain
        GestionnaireMenus.liste[2] = None


    def montrer():
        if GestionnaireMenus.liste[1] is None:
            application.quit()
            return

        GestionnaireMenus.liste[1]


    def maintenant() -> Menu:
        return GestionnaireMenus.liste[1]