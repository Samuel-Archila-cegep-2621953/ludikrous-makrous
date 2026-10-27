from menu import Menu
from musique import Musique
from types_musique import TypesMusique
from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from ursina.prefabs.window_panel import WindowPanel
from ursina.prefabs.input_field import InputField
from gestionnaire_langues import GestionnaireLangues as Langues
from gestionnaire_menus import GestionnaireMenus as GM
from utilitaires import (ordonner_boutons)
from config import Config
from constantes import LEN_MAX_NOM

class QuelquesMenus:
    COULEUR_BASE = color.rgba(130/255, 69/255, 16/255, 0.6)
    COULEUR_SURVOL = color.rgba(251/255, 119/255, 5/255, 0.8)

    @staticmethod
    def menu_principal() -> Menu:
        import __main__ as main
        LANGUE = Langues.LANGUE

        L_BOUTON = 0.5
        H_BOUTON = 0.06
        DEBUT_Y_BOUTONS: float = -0.13
        D_BOUTONS = 0.07
        #COULEUR_BASE = color.rgba(130/255, 69/255, 16/255, 0.6)
        COULEUR_BASE = color.rgba(0, 0, 0, 0.6)
        COULEUR_SURVOL = color.rgba(251/255, 119/255, 5/255, 0.8)
        ALPHA = 0.9

        _btn_commencer = Button(
            text=Langues.obtenir("menu_principal.boutons.jouer_seul", LANGUE),
            scale=(L_BOUTON, H_BOUTON),
            on_click=main.commencer_jeu,
        )

        _btn_heberger = Button(
            text=Langues.obtenir("menu_principal.boutons.heberger", LANGUE),
            scale=(L_BOUTON, H_BOUTON),
            on_click=main.commencer_jeu,
        )

        _btn_en_ligne = Button(
            text=Langues.obtenir("menu_principal.boutons.en_ligne", LANGUE),
            scale=(L_BOUTON, H_BOUTON),
            on_click= Func(GM.ajouter_et_montrer, QuelquesMenus.menu_multijoueur()),
        )

        _btn_config = Button(
            text=Langues.obtenir("menu_principal.boutons.config", LANGUE),
            scale=(L_BOUTON, H_BOUTON),
            on_click=Func(GM.ajouter_et_montrer, QuelquesMenus.menu_configuration()),
        )

        _btn_fermer = Button(
            text=Langues.obtenir("menu_principal.boutons.fermer", LANGUE),
            scale=(L_BOUTON, H_BOUTON),
            on_click=main.terminer_jeu,
            alpha = 0.5
        )

        _logo_titre = Entity(
            texture="ressources/textures/titre_vrai",
            origin=(0, 0),
            y=0.2,
            model="quad",
            scale=(1, 0.5),
        )

        _btn = ordonner_boutons([_btn_commencer, _btn_en_ligne, _btn_heberger, _btn_config, _btn_fermer], D_BOUTONS, H_BOUTON, L_BOUTON, DEBUT_Y_BOUTONS, COULEUR_BASE, COULEUR_SURVOL, 0)
        # Quand la fonction ordonner_boutons() modifie scale, le texte n'est pas montré correctement. Je ne sais pas pourquoi.

        return Menu(
            "principal",
            "matte-black", 
            Musique(TypesMusique.MENU_PRINCIPAL, autoplay= False), 
            _btn,
            [_logo_titre],
        )


    @staticmethod
    def menu_configuration():
        import __main__ as main

        L_BOUTON = 0.5
        H_BOUTON = 0.06
        DEBUT_Y_BOUTONS: float = -0.13
        D_BOUTONS = 0.07
        COULEUR_BASE = color.rgba(0, 0, 0, 0.8)
        #COULEUR_BASE = color.rgba(23/255, 21/255, 21/255, 0.8)
        COULEUR_SURVOL = QuelquesMenus.COULEUR_SURVOL


        _changements: dict[str, str] = {}

        def __changer_langue(l: str):
            _changements["langue"] = l

        def __changer_nom_affichage(nom: str):
            _changements["nom_affichage"] = nom

        def __appliquer_changements():
            __changer_nom_affichage(_saisir.text)
            try:
                Langues.changer(_changements["langue"])
            except:
                pass

            try:
                Config.changer_nom(_changements["nom_affichage"])
            except:
                pass
                

        _boutons_lang: list[Button] = []

        for l in Langues.liste:
            _boutons_lang.append(DropdownMenuButton(
                text = Langues.obtenir("nom", l),
                color = COULEUR_BASE,
                x = 0,
                #on_click = Func(Langues.changer, l),
                on_click = Func(__changer_langue, l),
                highlight_color = COULEUR_SURVOL
            ))

        _deroulant_langue = DropdownMenu(
            text=Langues.obtenir("menu_config.boutons.langues", Langues.LANGUE),
            scale = (L_BOUTON, H_BOUTON),
            buttons = _boutons_lang,
        )
        _deroulant_langue.x = -0.25
        _deroulant_langue.y = -0.2

        _saisir = InputField(
            default_value = Config.json()["Client"]["nom_affichage"],
            origin = (0,0),
            position = (0, -0.15),
            character_limit = LEN_MAX_NOM,
            tooltip = Tooltip(Langues.obtenir("menu_config.texte.nom_affichage", Langues.LANGUE))
            #scale = (L_BOUTON, H_BOUTON)
        )
        _etiquette_saisir = Text(
            Langues.obtenir("menu_config.texte.nom_affichage", Langues.LANGUE),
            origin = (0,0),
            position = (_saisir.x - 0.15, _saisir.y + 0.05)
        )

        """
        _menu_nom = WindowPanel(
            title = None,
            content = (
                Text("Paramètres"),
                #_saisir,
                #_deroulant_langue
            ),
            popup = False,
        )
        _menu_nom.y = _menu_nom.panel.scale_y / 2 * _menu_nom.scale_y#
        #_menu_nom.x = -0.25
        _menu_nom.origin = (0,0)
        _menu_nom.collider = None
        _menu_nom.disable()
        _menu_nom.layout()
        """

        _btn_confirmer = Button(
            #text = Langues.obtenir("menu_config.boutons.confirmer"),
            text = Langues.obtenir("menu_config.boutons.confirmer", Langues.LANGUE),
            scale = (L_BOUTON, H_BOUTON),
            color = COULEUR_BASE,
            highlight_color = COULEUR_SURVOL,
            on_click = __appliquer_changements,
            origin = (0,0),
            position = (0, 0.3)
        )
        
        return Menu("config", "matte-black", Musique(TypesMusique.MENU_PRINCIPAL, autoplay = False), [_btn_confirmer], [_saisir], [_etiquette_saisir], [_deroulant_langue], False)


    @staticmethod
    def menu_multijoueur():
        import __main__ as main

        L_BOUTON = 0.5
        H_BOUTON = 0.06
        DEBUT_Y_BOUTONS: float = -0.13
        D_BOUTONS = 0.07
        COULEUR_BASE = color.rgba(0, 0, 0, 0.8)
        #COULEUR_BASE = color.rgba(23/255, 21/255, 21/255, 0.8)
        COULEUR_SURVOL = QuelquesMenus.COULEUR_SURVOL

        _saisir_ip = InputField(
            default_value = Config.json()["Client"]["ip"],
            origin = (0,0),
            position = (0, -0.15),
            #character_limit = L
            tooltip = Tooltip("IP")
        )

        _etiquette_saisir_ip = Text(
            Langues.obtenir("menu_multijoueur.texte.ip"),
            origin = (0,0),
            position = (_saisir_ip.x - 0.23, _saisir_ip.y + 0.05)
        )

        def __changer_ip():
            Config.changer_ip(_saisir_ip.text)

        _btn_connection = Button(
            text=Langues.obtenir("menu_multijoueur.boutons.connection", Langues.LANGUE),
            scale=(L_BOUTON, H_BOUTON),
            on_click=__changer_ip,
            highlight_color = COULEUR_SURVOL,
            alpha = 0.5,
            y = -0.24,
        )

        return Menu("multijoueur", "matte-black", boutons = [_btn_connection], autres = [_saisir_ip], textes = [_etiquette_saisir_ip], enabled = False)