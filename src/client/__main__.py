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
from gestionnaire_menus import GestionnaireMenus as Gm


#if __name__ == "__main__":
_client = Client()

window.borderless = False
window.vsync = False
window.size = (1280, 720)
#window.fullscreen = True
#window.main_monitor = window.monit
#window.show_ursina_splash = True
#window.size = (1280, 720)

Langues.de_config()
LANGUE = Langues.LANGUE

app = Ursina(icon=obtenir_ressources() / "logo.ico", title="Ludikrous Makrous")

pivot = Entity()
DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, -45, 45))

#menu_principal = Entity(parent=camera.ui)

Text.default_font = "ressources/polices/CraftyGirls-Regular.ttf"


def terminer_jeu():
    print("Fermeture du jeu...")
    application.quit()


def commencer_jeu():
    Gm.maintenant().cacher()
    #musique.fade_out(duration=0.7)

    ciel_texte = load_texture("ressources/textures/ciel")
    _ciel = Sky(texture=ciel_texte)
    _monde = monde.Monde(8, 8)



    _moi = joueur_client.JoueurClient(_client)
    #_moi.musique.fade_in(duration=0.7)


Gm.ajouter_et_montrer(QuelquesMenus.menu_principal())
#print(Langues.trouver_clef("Paramètres"))
#Gm.montrer()
#_principal = QuelquesMenus.menu_principal()


# app.wireframe_on()

#musique_titre = Musique(TypesMusique.MENU_PRINCIPAL)
#TODO WHY WAS THIS UNCOMMENTED ^ ^ ^ ^ ^ 
# jsp, bonne question

def input(key):
    """
    if Gm.nom_maintenant() == "config" and Gm.nom_passe() == "principal":
        if key == "escape":
            Gm.retourner_et_montrer(True)

    elif Gm.nom_maintenant() == "multijoueur" and Gm.nom_passe() == "principal":
        if key == "escape":
            Gm.retourner_et_montrer(True)

    elif Gm.nom_maintenant() == "heberger" and Gm.nom_passe() == "principal":
        if key == "escape":
            Gm.retourner_et_montrer(True)

    """
    if Gm.nom_passe() is not None and Gm.nom_passe() == "principal":
        if key == "escape":
            Gm.retourner_et_montrer()

    if held_keys['t'] and held_keys["shift"] and held_keys["control"]:
        Gm.remplacer_musique("principal")

app.run()

