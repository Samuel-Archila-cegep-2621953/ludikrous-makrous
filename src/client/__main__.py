from client_serveur import Client
from ursina import *
from ursina.prefabs.health_bar import HealthBar
import joueur_client
from ressources import obtenir_ressources
from gestionnaire_langues import GestionnaireLangues as Langues
import monde
from musique import Musique
from types_musique import TypesMusique
from sons import Son
from menus import QuelquesMenus
from gestionnaire_menus import GestionnaireMenus as GM

#if __name__ == "__main__":
_client = Client()

window.borderless = False
window.vsync = False
#window.fullscreen = True
#window.main_monitor = window.monit
#window.show_ursina_splash = True
#window.size = (1280, 720)

Langues.de_config()
LANGUE = Langues.LANGUE

app = Ursina(icon=obtenir_ressources() / "logo.ico", title="Ludikrous Makrous")

#menu_principal = Entity(parent=camera.ui)

Text.default_font = "ressources/polices/CraftyGirls-Regular.ttf"


def terminer_jeu():
    print("Fermeture du jeu...")
    application.quit()


def commencer_jeu():
    GM.maintenant().cacher()
    #musique.fade_out(duration=0.7)

    ciel_texte = load_texture("ressources/textures/ciel")
    _ciel = Sky(texture=ciel_texte)
    _monde = monde.Monde(8, 8)



    _moi = joueur_client.JoueurClient(_client)
    #_moi.musique.fade_in(duration=0.7)


GM.ajouter(QuelquesMenus.menu_principal())
#print(Langues.trouver_clef("Paramètres"))
#GM.montrer()
#_principal = QuelquesMenus.menu_principal()


# app.wireframe_on()
"""
bg = Entity(
    parent=menu_principal,
    model="quad",
    scale=(window.aspect_ratio, 1),
    z=1,
    texture="ressources/textures/matte-black",
)
btn_commencer = Button(
    #text="Commencer",
    text=Langues.obtenir("menu_principal.boutons.commencer", LANGUE),
    parent=menu_principal,
    scale=(0.25, 0.075),
    y=-0.2,
    on_click=commencer_jeu,
    color=color.azure,
)
# btn_fermer = Button(text="Fermer", parent=menu_principal, scale=(0.25, 0.075), y=-0.29, on_click=terminer_jeu, color=color.blue)
btn_fermer = Button(
    #text="Fermer",
    text=Langues.obtenir("menu_principal.boutons.fermer", LANGUE),
    parent=menu_principal,
    scale=(0.25, 0.075),
    y=-0.29,
    on_click=terminer_jeu,
    color=color.red,
)
titre = Entity(
    texture="ressources/textures/titre_vrai",
    parent=menu_principal,
    origin=(0, 0),
    y=0.2,
    model="quad",
    scale=(1, 0.5),
)


musique_titre = Musique(TypesMusique.MENU_PRINCIPAL)
"""
pivot = Entity()
DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, -45, 45))

def input(key):
    if GM.nom_maintenant() == "config" and GM.nom_passe() == "principal":
        if key == "escape":
            GM.retourner_et_montrer()

    elif GM.nom_maintenant() == "multijoueur" and GM.nom_passe() == "principal":
        if key == "escape":
            GM.retourner_et_montrer()

    elif GM.nom_maintenant() == "heberger" and GM.nom_passe() == "principal":
        if key == "escape":
            GM.retourner_et_montrer()
    """
    if GM.nom_passe() == "principal":
        if key == "escape":
            GM.retourner_et_montrer()
    """

app.run()

