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

#musique_titre = Musique(TypesMusique.MENU_PRINCIPAL)
#TODO WHY WAS THIS UNCOMMENTED ^ ^ ^ ^ ^ 
pivot = Entity()
DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, -45, 45))

def input(key):
    if GM.nom_maintenant() == "config" and GM.nom_passe() == "principal":
        if key == "escape":
            GM.retourner_et_montrer(True)

    elif GM.nom_maintenant() == "multijoueur" and GM.nom_passe() == "principal":
        if key == "escape":
            GM.retourner_et_montrer(True)

    elif GM.nom_maintenant() == "heberger" and GM.nom_passe() == "principal":
        if key == "escape":
            GM.retourner_et_montrer(True)

    #if held_keys['t'] and held_keys["shift"]:
    if key == "t":
        print("Arreter musique")
        GM.remplacer_musique()
    """
    if GM.nom_passe() == "principal":
        if key == "escape":
            GM.retourner_et_montrer()
    """

app.run()

