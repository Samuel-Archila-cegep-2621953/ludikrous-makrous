from ..menu import Menu
from ..musique import Musique
from ..types_musique import TypesMusique
from ursina import *
from ..__main__ import * # commencer_jeu() etc

class QuelquesMenus:
    LANGUE = "fr"

    @staticmethod
    def menu_principal():
        _btn_commencer = Button(
            text=Langues.obtenir("menu_principal.boutons.jouer_seul", LANGUE),
            scale=(0.25, 0.075),
            y=-0.2,
            on_click=commencer_jeu,
            color=color.azure,
        )

        _btn_heberger = Button(
            text=Langues.obtenir("menu_principal.boutons.heberger", LANGUE),
            scale=(0.25, 0.075),
            y=-0.29,
            on_click=commencer_jeu,
            color=color.azure,
        )

        _btn_en_ligne = Button(
            text=Langues.obtenir("menu_principal.boutons.en_ligne", LANGUE),
            scale=(0.25, 0.075),
            y=-0.38,
            on_click=commencer_jeu,
            color=color.azure,
        )

        _btn_config = Button(
            text=Langues.obtenir("menu_principal.boutons.config", LANGUE),
            scale=(0.25, 0.075),
            y=-0.47,
            on_click=QuelquesMenus.menu_configuration,
            color=color.azure,
        )

        _btn_fermer = Button(
            text=Langues.obtenir("menu_principal.boutons.fermer", LANGUE),
            scale=(0.25, 0.075),
            y=-0.56,
            on_click=terminer_jeu,
            color=color.red,
        )

        _menu = Menu(
            "matte-black", 
            Musique(TypesMusique.MENU_PRINCIPAL), 
            [_btn_commencer, _btn_config, _btn_fermer, _btn_en_ligne, _btn_heberger]
        )


    @staticmethod
    def menu_configuration():
        pass
