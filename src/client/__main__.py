from client_serveur import Client
from ursina import *
import joueur_client
from ressources import obtenir_ressources
from gestionnaire_langues import GestionnaireLangues

if __name__ == '__main__':
    _client = Client()

    window.borderless = False

    app = Ursina(icon=obtenir_ressources() / 'logo.ico', title="Ludikrous Makrous")

    sky_text = load_texture('ressources/textures/end')
    sky = Sky(texture=sky_text)

    menu_principal = Entity(parent=camera.ui)

    Text.default_font = 'ressources/polices/CraftyGirls-Regular.ttf'

    def terminer_jeu():
        application.quit()

    def commencer_jeu():
        menu_principal.disable()
        musique_titre.fade_out(duration=0.7)

        plateforme = Entity(model='cube', color=rgb(25, 205, 225), scale=(10, 1, 10), position=(0, -2, 0),collider='box')
        joueur_client.JoueurClient(_client)

    #app.wireframe_on()
    #print("\033[92m" + "Succes" + "\033[0m")
    bg = Entity(parent=menu_principal, model='quad', scale=(window.aspect_ratio, 1), z=1, texture='ressources/textures/wk')
    btn_commencer = Button(text='Jouer', parent=menu_principal, scale=(0.25, 0.075), y=-0.2, on_click=commencer_jeu, color=color.blue)
    btn_fermer = Button(text='Fermer', parent=menu_principal, scale=(0.25, 0.075), y=-0.29, on_click=terminer_jeu, color=color.blue)
    titre = Entity(texture='ressources/textures/titre_vrai', parent=menu_principal, origin=(0, 0), y=0.2, model='quad', scale=(1, 0.5))

    musique_titre = Audio('ressources/sons/twin_princes.ogg', loop=True, autoplay=True, volume=0.7)



    plateforme = Entity(model='cube', color=rgb(255, 255, 255), scale=(10,1,10), position=(0,-2,0), collider='box')

    app.run()