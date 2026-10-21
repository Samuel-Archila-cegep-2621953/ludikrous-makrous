from client_serveur import Client
from ursina import *
import joueur_client
from ressources import obtenir_ressources

if __name__ == '__main__':
    _client = Client()

    window.borderless = False

    app = Ursina(icon=obtenir_ressources() / 'logo.ico', title="Ludikrous Makrous")

    plateforme = Entity(model='cube', color=rgb(255, 255, 255), scale=(10,1,10), position=(0,-2,0), collider='box')
    joueur_client.JoueurClient(_client)
    app.run()