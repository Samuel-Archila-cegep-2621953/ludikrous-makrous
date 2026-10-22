import socket
import threading
import time
import monde_serveur
import json

"""
TODO: Changer le serveur pour qu'il soit async
"""

CONFIGURATION_SERVEUR = {
    "IP": '10.70.60.14',
    "Port": 24113
}

class Serveur:
    def __init__(self):
        self.__serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__serveur.bind((CONFIGURATION_SERVEUR["IP"], CONFIGURATION_SERVEUR["Port"]))
        self.__serveur.listen(5)

        self.__monde_serveur = monde_serveur.MondeServeur()

        print(f"Serveur lancé sur {CONFIGURATION_SERVEUR["IP"]}:{CONFIGURATION_SERVEUR["Port"]}")

    def __gerer_client(self, socket_client: socket.socket):
        _requete = socket_client.recv(1024)
        # print(f"[+] Reçu: {_requete}")

        socket_client.send(self.__monde_serveur.recevoir_client(_requete).encode())

        socket_client.close()

    def boucle_principale(self):

        _temps_entre_update = 0.0
        _debut = 0.0
        _fin = 0.0

        while True:
            _client, _addresse = self.__serveur.accept()

            _gerant_de_client = threading.Thread(target=self.__gerer_client, args=(_client,))
            _gerant_de_client.start()


            _temps_entre_update = _fin - _debut

            _debut = time.time()
            self.__monde_serveur.mise_a_jour_jeu(_temps_entre_update)
            _fin = time.time()




