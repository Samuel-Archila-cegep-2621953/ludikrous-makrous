from menu import Menu
from array import array
from ursina import *
from gestionnaire_langues import GestionnaireLangues as Langues

# Peut-être ça sera utilisé

class GestionnaireMenus:
    liste: list[Menu] = [None, None, None]

    @staticmethod
    def ajouter(prochain: Menu):
        """
        Ajoute le prochain menu après la fin de celui qui est activé en ce moment
        Args: 
            prochain (Menu): Le prochain menu à montrer

        """
        GestionnaireMenus.liste[0] = GestionnaireMenus.liste[1]
        GestionnaireMenus.liste[1] = prochain
        GestionnaireMenus.liste[1].musique.stop()
        GestionnaireMenus.liste[2] = None


    @staticmethod
    def montrer():
        if GestionnaireMenus.liste[1] is None:
            application.quit()
            return

        """
        if Langues.LANGUE != Langues.LANGUE_AVANT:
            for m in GestionnaireMenus.liste:
                if m is not None:
                    m.maj_langue()
        """

        GestionnaireMenus.liste[1].montrer()


    @staticmethod
    def cacher():
        GestionnaireMenus.liste[1].cacher()


    @staticmethod
    def maintenant() -> Menu:
        return GestionnaireMenus.liste[1]


    @staticmethod
    def ajouter_et_montrer(menu: Menu):
        GestionnaireMenus.liste[1].cacher()
        GestionnaireMenus.ajouter(menu)
        GestionnaireMenus.montrer()
        #GestionnaireMenus.liste[1]


    @staticmethod
    def retourner():
        _passe = GestionnaireMenus.liste[0]
        #_passe.disable()
        GestionnaireMenus.liste[0] = GestionnaireMenus.liste[1]
        GestionnaireMenus.liste[1] = _passe
        GestionnaireMenus.liste[2] = None



    @staticmethod
    def retourner_et_montrer():
        GestionnaireMenus.cacher()
        GestionnaireMenus.retourner()
        GestionnaireMenus.montrer()


    @staticmethod
    def nom_maintenant() -> str:
        return GestionnaireMenus.liste[1].nom


    @staticmethod
    def nom_prochain() -> str:
        return GestionnaireMenus.liste[2].nom


    @staticmethod
    def nom_passe() -> str:
        return GestionnaireMenus.liste[0].nom