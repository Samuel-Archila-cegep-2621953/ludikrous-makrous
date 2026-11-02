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
        #GestionnaireMenus.liste[1].arreter_musique()
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
    def cacher(garder_musique: bool = False):
        GestionnaireMenus.liste[1].cacher(garder_musique = garder_musique)


    @staticmethod
    def maintenant() -> Menu:
        return GestionnaireMenus.liste[1]


    @staticmethod
    def ajouter_et_montrer(menu: Menu, garder_musique: bool = False):
        GestionnaireMenus.liste[1].cacher(garder_musique = garder_musique)
        GestionnaireMenus.ajouter(menu)
        GestionnaireMenus.montrer()
        #GestionnaireMenus.liste[1]


    @staticmethod
    def retourner():
        _passe = GestionnaireMenus.liste[0]
        GestionnaireMenus.liste[0] = GestionnaireMenus.liste[1]
        GestionnaireMenus.liste[1] = _passe
        GestionnaireMenus.liste[2] = None



    @staticmethod
    def retourner_et_montrer(garder_musique: bool = False):
        GestionnaireMenus.cacher(garder_musique)
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


    @staticmethod
    def remplacer_musique(nom: str):
        #print(GestionnaireMenus.liste[1].nom)
        for m in GestionnaireMenus.liste:
            if m is not None and m.nom == nom: m.musique.arreter()


    @staticmethod
    def __idx_maintenant() -> int:
        return len(GestionnaireMenus.liste) - 2


    @staticmethod
    def __idx_prochain() -> int:
        return len(GestionnaireMenus.liste) + 1