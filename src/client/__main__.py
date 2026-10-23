from client_serveur import Client
from ursina import *
import joueur_client
from ressources import obtenir_ressources
from gestionnaire_langues import GestionnaireLangues
import monde

if __name__ == "__main__":
    _client = Client()

    window.borderless = False
    window.vsync = True
    window.size = (1280, 720)

    LANGUE = "fr"

    app = Ursina(icon=obtenir_ressources() / "logo.ico", title="Ludikrous Makrous")

    menu_principal = Entity(parent=camera.ui)

    Text.default_font = "ressources/polices/CraftyGirls-Regular.ttf"

    def terminer_jeu():
        application.quit()

    def commencer_jeu():
        menu_principal.disable()
        #musique_titre.fade_out(duration=0.7)

        ciel_texte = load_texture("ressources/textures/end-rect")
        ciel = Sky(texture=ciel_texte)
        _monde = monde.Monde(8, 8)
        #ground = Entity(model='cube', position=(0,0,0), scale=(2, 0.5, 2), color=color.white, collider="box")
        joueur_client.JoueurClient(_client)

    # app.wireframe_on()
    # print("\033[92m" + "Succes" + "\033[0m")
    bg = Entity(
        parent=menu_principal,
        model="quad",
        scale=(window.aspect_ratio, 1),
        z=1,
        texture="ressources/textures/matte-black",
    )
    btn_commencer = Button(
        #text="Commencer",
        text=GestionnaireLangues.obtenir("menu_principal.boutons.commencer", LANGUE),
        parent=menu_principal,
        scale=(0.25, 0.075),
        y=-0.2,
        on_click=commencer_jeu,
        color=color.azure,
    )
    # btn_fermer = Button(text="Fermer", parent=menu_principal, scale=(0.25, 0.075), y=-0.29, on_click=terminer_jeu, color=color.blue)
    btn_fermer = Button(
        #text="Fermer",
        text=GestionnaireLangues.obtenir("menu_principal.boutons.fermer", LANGUE),
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

    musique_titre = Audio(
        "ressources/sons/twin_princes.ogg", loop=True, autoplay=True, volume=0.7
    )

    pivot = Entity()
    DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, -45, 45))

    app.run()
