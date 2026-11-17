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
import socket
import hashlib
from time import sleep

class QuelquesMenus:
    COULEUR_BASE = color.rgba(130/255, 69/255, 16/255, 0.6)
    COULEUR_SURVOL = color.rgba(251/255, 119/255, 5/255, 0.8)

    @staticmethod
    def menu_principal() -> Menu:
        import __main__ as main
        LANGUE = Langues.LANGUE

        L_BOUTON = 0.5
        H_BOUTON = 0.06
        DEBUT_Y_BOUTONS: float = 0.17
        D_BOUTONS = 0.06
        #COULEUR_BASE = color.rgba(130/255, 69/255, 16/255, 0.6)
        COULEUR_BASE = color.rgba(0, 0, 0, 0.0)
        COULEUR_SURVOL = color.rgba(251/255, 119/255, 5/255, 0.0)
        ALPHA = 0.9

        _btn_commencer = Button(
            text=Langues.obtenir("menu_principal.boutons.jouer_seul", LANGUE),
            scale=(L_BOUTON, H_BOUTON),
            on_click=main.commencer_jeu,
        )

        _btn_heberger = Button(
            text=Langues.obtenir("menu_principal.boutons.heberger", LANGUE),
            scale=(L_BOUTON, H_BOUTON),
            on_click=Func(GM.ajouter_et_montrer, QuelquesMenus.menu_heberger(), True),
        )

        _btn_en_ligne = Button(
            text=Langues.obtenir("menu_principal.boutons.en_ligne", LANGUE),
            scale=(L_BOUTON, H_BOUTON),
            on_click= Func(GM.ajouter_et_montrer, QuelquesMenus.menu_multijoueur(), True),
        )

        _btn_config = Button(
            text=Langues.obtenir("menu_principal.boutons.config", LANGUE),
            scale=(L_BOUTON, H_BOUTON),
            on_click=Func(GM.ajouter_et_montrer, QuelquesMenus.menu_configuration(), True),
        )

        _btn_fermer = Button(
            text=Langues.obtenir("menu_principal.boutons.fermer", LANGUE),
            scale=(L_BOUTON, H_BOUTON),
            on_click=main.terminer_jeu,
            alpha = 0.5
        )

        _logo_titre = Entity(
            texture="ressources/textures/titre_vrai",
            origin=(1, -1),
            position=(0.25,0.15),
            model="quad",
            scale=(1/1.3, 0.3/1.3),
        )

        _btn = ordonner_boutons([_btn_commencer, _btn_en_ligne, _btn_heberger, _btn_config, _btn_fermer], D_BOUTONS, H_BOUTON, L_BOUTON, DEBUT_Y_BOUTONS, COULEUR_BASE, COULEUR_SURVOL, 0)
        # Quand la fonction ordonner_boutons() modifie scale, le texte n'est pas montré correctement. Je ne sais pas pourquoi.

        return Menu(
            "principal",
            "matte-black", 
            Musique(TypesMusique.MENU_PRINCIPAL, autoplay= False), 
            _btn,
            [_logo_titre],
            enabled = False
        )


    @staticmethod
    def menu_configuration() -> Menu:
        import __main__ as main

        L_BOUTON = 0.5
        H_BOUTON = 0.06
        DEBUT_Y_BOUTONS: float = -0.13
        D_BOUTONS = 0.07
        COULEUR_BASE = color.rgba(0, 0, 0, 0.8)
        #COULEUR_BASE = color.rgba(23/255, 21/255, 21/255, 0.8)
        COULEUR_SURVOL = QuelquesMenus.COULEUR_SURVOL


        _changements: dict[str, str] = {}

        def __changer_nom_utilisateur(nom: str):
            _changements["nom_utilisateur"] = nom

        def __changer_mdp(mdp: str):
            if mdp == '':
                _changements["mot_de_passe_hache"] = Config.json()["Client"]["mot_de_passe_hache"]
                return

            #print(mdp)
            #mpd = "Password1"
            """
            _ = hashlib.sha256(
                hashlib.sha256(
                    mpd.encode()
                ).digest
            ).hexdigest()
            """
            #_changements["mot_de_passe_hache"] = hashlib.sha256(hashlib.sha256(mdp.encode()).digest()).hexdigest()
            _changements["mot_de_passe_hache"] = hashlib.sha256(mdp.encode()).hexdigest()
            # _changements["mot_de_passe_hache"] = hash

        def __changer_illumination(mode: str):
            pass

        def __changer_langue(l: str):
            _changements["langue"] = l

        def __changer_nom_affichage(nom: str):
            _changements["nom_affichage"] = nom

        def __appliquer_changements():
            __changer_nom_affichage(_saisir_nom_affichage.text)
            __changer_nom_utilisateur(_saisir_nom_utilisateur.text)
            __changer_mdp(_saisir_mdp.text)
            try:
                Langues.changer(_changements["langue"])
            except:
                pass

            try:
                Config.changer_nom_affichage(_changements["nom_affichage"])
            except:
                pass

            try:
                Config.changer_nom_utilisateur(_changements["nom_utilisateur"])
            except:
                pass

            try:
                Config.changer_mdp(_changements["mot_de_passe_hache"])
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

        _saisir_nom_affichage = InputField(
            default_value = Config.json()["Client"]["nom_affichage"],
            origin = (0,0),
            position = (0, -0.15),
            character_limit = LEN_MAX_NOM,
            tooltip = Tooltip(Langues.obtenir("menu_config.texte.nom_affichage", Langues.LANGUE))
            #scale = (L_BOUTON, H_BOUTON)
        )
        _etiquette_saisir_nom_affichage = Text(
            Langues.obtenir("menu_config.texte.nom_affichage", Langues.LANGUE),
            origin = (0,0),
            position = (_saisir_nom_affichage.x - 0.15, _saisir_nom_affichage.y + 0.05)
        )

        _saisir_nom_utilisateur = InputField(
            default_value = Config.json()["Client"]["nom_utilisateur"],
            origin = (0,0),
            position = (0, 0.05), # TODO
            character_limit = LEN_MAX_NOM,
            tooltip = Tooltip(Langues.obtenir("menu_config.texte.nom_utilisateur", Langues.LANGUE))
            #scale = (L_BOUTON, H_BOUTON)
        )
        _etiquette_saisir_nom_utilisateur = Text(
            Langues.obtenir("menu_config.texte.nom_utilisateur", Langues.LANGUE),
            origin = (0,0),
            position = (_saisir_nom_utilisateur.x - 0.15, _saisir_nom_utilisateur.y + 0.05)
        )

        _saisir_mdp = InputField(
            #default_value = Config.json()["Client"]["mot_de_passe_hache"],
            hide_content = True,
            origin = (0,0),
            position = (0, -0.05), # TODO
            character_limit = LEN_MAX_NOM,
            tooltip = Tooltip(Langues.obtenir("menu_config.texte.mot_de_passe", Langues.LANGUE))
            #scale = (L_BOUTON, H_BOUTON)
        )
        _etiquette_saisir_mdp = Text(
            Langues.obtenir("menu_config.texte.mot_de_passe", Langues.LANGUE),
            origin = (0,0),
            position = (_saisir_mdp.x - 0.15, _saisir_mdp.y + 0.05)
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
        
        #return Menu("config", "matte-black", Musique(TypesMusique.MENU_PRINCIPAL, autoplay = False), [_btn_confirmer], [_saisir], [_etiquette_saisir], [_deroulant_langue], False)
        return Menu(
            "config",
            "matte-black",
            None,
            [_btn_confirmer], 
            [_saisir_nom_affichage, _saisir_nom_utilisateur, _saisir_mdp], 
            [_etiquette_saisir_nom_affichage, _etiquette_saisir_nom_utilisateur, _etiquette_saisir_mdp], 
            [_deroulant_langue], 
            False
        )


    @staticmethod
    def menu_multijoueur() -> Menu:
        import __main__ as main
        from utilitaires import verifier_ip, verifier_port

        L_BOUTON = 0.5
        H_BOUTON = 0.06
        DEBUT_Y_BOUTONS: float = -0.13
        D_BOUTONS = 0.07
        COULEUR_BASE = color.rgba(0, 0, 0, 0.8)
        #COULEUR_BASE = color.rgba(23/255, 21/255, 21/255, 0.8)
        COULEUR_SURVOL = QuelquesMenus.COULEUR_SURVOL
        CHARS_PERMIS = "0123456789"

        _saisir_ip = InputField(
            default_value = Config.json()["Client"]["ip"],
            origin = (0,0),
            position = (0, -0.15),
            #character_limit = L
            #tooltip = Tooltip("IP")
            limit_content_to = CHARS_PERMIS + '.'
        )

        _etiquette_saisir_ip = Text(
            Langues.obtenir("menu_multijoueur.texte.ip", Langues.LANGUE),
            origin = (0,0),
            position = (_saisir_ip.x - 0.18, _saisir_ip.y + 0.05)
        )

        _saisir_port = InputField(
            default_value = str(Config.json()["Client"]["port"]).strip(),
            origin = (0,0),
            position = (0, -0.26),
            limit_content_to = CHARS_PERMIS
            #character_limit = L
            #tooltip = Tooltip("IP")
        )

        _etiquette_saisir_port = Text(
            Langues.obtenir("menu_multijoueur.texte.port", Langues.LANGUE),
            origin = (0,0),
            position = (_saisir_port.x - 0.22, _saisir_port.y + 0.05)
        )
        

        def _cacher_texte(t: Text):
            t.disable()

        def _afficher_erreur(k: str):
            _texte_erreur = Text(
                text = Langues.obtenir(k, Langues.LANGUE),
                origin = (0,0),
                position = (0,0),
                color = color.red,
            )
            invoke(_cacher_texte, _texte_erreur, delay = 2)

        def __changer_infos():
            import __main__ as main
            if not verifier_ip(_saisir_ip.text.strip()): # Vérifier si l'addresse ip est valide. Montre un message d'erreur si elle ne l'est pas
                _afficher_erreur("menu_multijoueur.texte.erreur_ip")
                return
            elif not verifier_port(_saisir_port.text.strip()):
                _afficher_erreur("menu_multijoueur.texte.erreur_port")
                return
                
            Config.changer_ip(_saisir_ip.text.strip())
            Config.changer_port(int(_saisir_port.text.strip()))
            GM.ajouter_et_montrer(QuelquesMenus.menu_attente(), True)
            #sleep(0.3)
            main.commencer_jeu()
            
            

        _btn_connection = Button(
            text=Langues.obtenir("menu_multijoueur.boutons.connection", Langues.LANGUE),
            scale=(L_BOUTON, H_BOUTON),
            on_click=__changer_infos,
            highlight_color = COULEUR_SURVOL,
            alpha = 0.5,
            y = _saisir_port.y - 0.1,
        )

        return Menu("multijoueur", "matte-black", boutons = [_btn_connection], autres = [_saisir_ip, _saisir_port], textes = [_etiquette_saisir_ip, _etiquette_saisir_port], enabled = False)


    def menu_attente():
        GRANDEUR_TEXTE = 3
        _texte = Text(
            text = Langues.obtenir("menu_attente.texte.attendez", Langues.LANGUE),
            origin = (0,0),
            position = (0,0),
            scale = GRANDEUR_TEXTE
        )

        return Menu("attente", "matte-black", textes = [_texte])


    @staticmethod
    def menu_heberger() -> Menu:
        import __main__ as main

        L_BOUTON = 0.5
        H_BOUTON = 0.06
        DEBUT_Y_BOUTONS: float = -0.13
        D_BOUTONS = 0.07
        COULEUR_BASE = color.rgba(0, 0, 0, 0.8)
        #COULEUR_BASE = color.rgba(23/255, 21/255, 21/255, 0.8)
        COULEUR_SURVOL = QuelquesMenus.COULEUR_SURVOL

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        _mon_ip = s.getsockname()[0]
        s.close()

        _texte_mon_ip = Text(
            text = Langues.obtenir("menu_heberger.texte.ip_local", Langues.LANGUE) + _mon_ip,
            origin = (0,0),
            position = (0,0)
        )

        #TODO!: Obtenir une liste de joueurs
        _liste_joueurs: list[str] = ["Big John", "Scarlett", "Makrous", "Ursino"]

        def __formatter_liste_joueurs(joueurs: list[str]) -> str:
            _joueurs_fmt: str = ""
            for j in joueurs:
                _joueurs_fmt += j + "\n"

            return _joueurs_fmt

        _joueurs_connectes = Text(
            text = Langues.obtenir("menu_heberger.texte.connections_presentes", Langues.LANGUE) + "\n" + __formatter_liste_joueurs(_liste_joueurs),
            origin = (0,0),
            position = (0,-0.1),
        )

        return Menu("heberger", "matte-black", textes = [_texte_mon_ip, _joueurs_connectes], enabled = False)