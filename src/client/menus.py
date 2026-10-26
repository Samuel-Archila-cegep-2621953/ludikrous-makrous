from menu import Menu
from musique import Musique
from types_musique import TypesMusique
from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from gestionnaire_langues import GestionnaireLangues as Langues
from gestionnaire_menus import GestionnaireMenus as GM
from utilitaires import (ordonner_boutons, changer_langue)

class QuelquesMenus:

    @staticmethod
    def menu_principal() -> Menu:
        import __main__ as main
        LANGUE = Langues.LANGUE

        L_BOUTON = 0.5
        H_BOUTON = 0.06
        DEBUT_Y_BOUTONS: float = -0.13
        D_BOUTONS = 0.07

        _btn_commencer = Button(
            text=Langues.obtenir("menu_principal.boutons.jouer_seul", LANGUE),
            scale=(L_BOUTON, H_BOUTON),
            on_click=main.commencer_jeu,
            color=color.azure,
        )

        _btn_heberger = Button(
            text=Langues.obtenir("menu_principal.boutons.heberger", LANGUE),
            scale=(L_BOUTON, H_BOUTON),
            on_click=main.commencer_jeu,
            color=color.azure,
        )

        _btn_en_ligne = Button(
            text=Langues.obtenir("menu_principal.boutons.en_ligne", LANGUE),
            scale=(L_BOUTON, H_BOUTON),
            on_click= main.commencer_jeu,
            color=color.azure,
        )

        _btn_config = Button(
            text=Langues.obtenir("menu_principal.boutons.config", LANGUE),
            scale=(L_BOUTON, H_BOUTON),
            on_click=Func(GM.ajouter_et_montrer, QuelquesMenus.menu_configuration()),
            color=color.azure,
        )

        _btn_fermer = Button(
            text=Langues.obtenir("menu_principal.boutons.fermer", LANGUE),
            scale=(L_BOUTON, H_BOUTON),
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

        _btn = ordonner_boutons([_btn_commencer, _btn_en_ligne, _btn_heberger, _btn_config, _btn_fermer], D_BOUTONS, H_BOUTON, L_BOUTON, DEBUT_Y_BOUTONS)
        # Quand la fonction ordonner_boutons() modifie scale, le texte n'est pas montré correctement. Je ne sais pas pourquoi.

        return Menu(
            "principal",
            "matte-black", 
            Musique(TypesMusique.MENU_PRINCIPAL), 
            _btn,
            [_logo_titre],
            #enabled=False
        )


    @staticmethod
    def menu_configuration():
        import __main__ as main

        L_BOUTON = 0.5
        H_BOUTON = 0.06
        DEBUT_Y_BOUTONS: float = -0.13
        D_BOUTONS = 0.07

        _ls_lang: list[str] = []

        _boutons_lang: list[Button] = []

        for l in Langues.liste:
            _boutons_lang.append(DropdownMenuButton(
                text = Langues.obtenir("nom", l),
                color = color.azure,
                #scale = (L_BOUTON, H_BOUTON),
                #origin = (0,0),
                x = 0,
                on_click = Func(changer_langue, l),
                #enabled = False
            ))

        _deroulant_langue = DropdownMenu(
            #origin = (0,0),
            y = -0.13,
            x = 0,
            text=Langues.obtenir("nom", Langues.LANGUE),
            scale = (L_BOUTON, H_BOUTON),
            buttons = _boutons_lang,
            #enabled = False
        )

        #TODO _btn_sauvegarder = Button()

        return Menu("config", "wk", Musique(TypesMusique.MENU_PRINCIPAL), [], [], [], [_deroulant_langue], False)