from menu import Menu
from array import array
from ursina import *
from gestionnaire_langues import GestionnaireLangues as Langues
from debogage import Debogage as Dbg

type Gm = GestionnaireMenus

class GestionnaireMenus:
    liste: list[Menu] = [None, None]
    ptr: int = 0

    @staticmethod
    def ajouter(prochain: Menu):
        """
        Ajoute le prochain menu après la fin de celui qui est activé en ce moment
        Args: 
            prochain (Menu): Le prochain menu à montrer

        """
        """
        GestionnaireMenus.liste[0] = GestionnaireMenus.liste[1]
        GestionnaireMenus.liste[1] = prochain
        #GestionnaireMenus.liste[1].arreter_musique()
        GestionnaireMenus.liste[2] = None
        """
        #GestionnaireMenus.liste[GestionnaireMenus.__idx_prochain()] = prochain
        #if GestionnaireMenus.liste[len(GestionnaireMenus.liste) - 1] is None: return
        if prochain is None: return

        GestionnaireMenus.liste[GestionnaireMenus.ptr + 1] = prochain
        if GestionnaireMenus.liste[len(GestionnaireMenus.liste) - 1] is not None:
            GestionnaireMenus.liste.append(None)


    @staticmethod
    def montrer():
        if GestionnaireMenus.liste[GestionnaireMenus.ptr] is None:
            print("Aucun menu à montrer. Fin du jeu.")
            application.quit()
            return

        """
        if Langues.LANGUE != Langues.LANGUE_AVANT:
            for m in GestionnaireMenus.liste:
                if m is not None:
                    m.maj_langue()
        """

        GestionnaireMenus.liste[GestionnaireMenus.ptr].montrer()


    @staticmethod
    def cacher(garder_musique: bool = False):
        GestionnaireMenus.liste[GestionnaireMenus.ptr].cacher(garder_musique = garder_musique)


    @staticmethod
    def maintenant() -> Menu:
        return GestionnaireMenus.liste[GestionnaireMenus.ptr]


    @staticmethod
    def ajouter_et_montrer(menu: Menu, garder_musique: bool = False):
        if GestionnaireMenus.liste[GestionnaireMenus.ptr] is not None:
            GestionnaireMenus.liste[GestionnaireMenus.ptr].cacher(garder_musique = garder_musique)


        GestionnaireMenus.ajouter(menu)
        GestionnaireMenus.avancer()
        GestionnaireMenus.montrer()

        Dbg.info(GestionnaireMenus.liste, 4)


    @staticmethod
    def retourner(n: int = 1):
        """
        _passe = GestionnaireMenus.liste[0]
        GestionnaireMenus.liste[0] = GestionnaireMenus.liste[1]
        GestionnaireMenus.liste[1] = _passe
        GestionnaireMenus.liste[2] = None
        """
        GestionnaireMenus.ptr -= n


    @staticmethod
    def avancer(n: int = 1):
        GestionnaireMenus.ptr += n


    @staticmethod
    def retourner_et_montrer(garder_musique: bool = False):
        GestionnaireMenus.cacher(garder_musique)
        GestionnaireMenus.retourner()
        GestionnaireMenus.montrer()


    @staticmethod
    def nom_maintenant() -> str:
        return GestionnaireMenus.liste[GestionnaireMenus.ptr].nom


    @staticmethod
    def nom_prochain() -> str:
        return GestionnaireMenus.liste[GestionnaireMenus.ptr + 1].nom


    @staticmethod
    def nom_passe() -> str | None:
        if GestionnaireMenus.liste[GestionnaireMenus.ptr - 1] is not None:
            return GestionnaireMenus.liste[GestionnaireMenus.ptr - 1].nom
        return None


    @staticmethod
    def remplacer_musique(nom: str):
        #print(GestionnaireMenus.liste[1].nom)
        for m in GestionnaireMenus.liste:
            if m is not None and m.nom == nom: m.musique.arreter()


    @staticmethod
    def __idx_maintenant() -> int:
        return GestionnaireMenus.ptr


    @staticmethod
    def __idx_prochain() -> int:
        return GestionnaireMenus.ptr + 1


    @staticmethod
    def chercher_nom(nom: str) -> int | None:
        for m, idx in enumerate(GestionnaireMenus.liste):
            if m is not None and m.nom == nom: return idx
        return None