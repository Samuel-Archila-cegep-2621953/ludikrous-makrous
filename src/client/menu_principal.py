from menu import Menu
from musique import Musique
from types_musique import TypesMusique
from ursina import *
from gestionnaire_langues import GestionnaireLangues as Langues

class QuelquesMenus:

    @staticmethod
    def menu_principal() -> Menu:
        import __main__ as main
        LANGUE = main.LANGUE

        L_BOUTON = 0.5
        H_BOUTON = 0.06
        DEBUT_Y_BOUTONS: float = -0.13
        D_BOUTONS = 0.07

        _btn_commencer = Button(
            text=Langues.obtenir("menu_principal.boutons.jouer_seul", LANGUE),
            scale=(L_BOUTON, H_BOUTON),
            y=DEBUT_Y_BOUTONS,
            on_click=main.commencer_jeu,
            color=color.azure,
        )

        _btn_heberger = Button(
            text=Langues.obtenir("menu_principal.boutons.heberger", LANGUE),
            scale=(L_BOUTON, H_BOUTON),
            y=DEBUT_Y_BOUTONS - D_BOUTONS,
            on_click=main.commencer_jeu,
            color=color.azure,
        )

        _btn_en_ligne = Button(
            text=Langues.obtenir("menu_principal.boutons.en_ligne", LANGUE),
            scale=(L_BOUTON, H_BOUTON),
            y=DEBUT_Y_BOUTONS - 2 * D_BOUTONS,
            on_click= main.commencer_jeu,
            color=color.azure,
        )

        _btn_config = Button(
            text=Langues.obtenir("menu_principal.boutons.config", LANGUE),
            scale=(L_BOUTON, H_BOUTON),
            y=DEBUT_Y_BOUTONS - 3 * D_BOUTONS,
            on_click=QuelquesMenus.menu_configuration,
            color=color.azure,
        )

        _btn_fermer = Button(
            text=Langues.obtenir("menu_principal.boutons.fermer", LANGUE),
            scale=(L_BOUTON, H_BOUTON),
            y=DEBUT_Y_BOUTONS - 4 * D_BOUTONS,
            on_click=main.terminer_jeu,
            color=color.red,
        )

        _logo_titre = Entity(
            texture="ressources/textures/titre_vrai",
            #parent=main.menu_principal,
            origin=(0, 0),
            y=0.2,
            model="quad",
            scale=(1, 0.5),
            #z = 1.00001
        )

        return Menu(
            "matte-black", 
            Musique(TypesMusique.MENU_PRINCIPAL), 
            [_btn_commencer, _btn_config, _btn_fermer, _btn_en_ligne, _btn_heberger],
            [_logo_titre]
        )


    @staticmethod
    def menu_configuration():
        pass
