import socket
import threading
import time
import monde_serveur

"""
TODO: Changer le serveur pour qu'il soit async
"""

CONFIGURATION_SERVEUR = {
    "IP": '127.0.0.1',
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
        requete = socket_client.recv(1024)
        print(f"[+] Reçu: {requete}")

        self.__monde_serveur.recevoir_client(requete)

        socket_client.send("Ping received".encode())
        socket_client.close()

    def boucle_principale(self):

        temps_entre_update = 0.0
        debut = 0.0
        fin = 0.0

        while True:



            client, addresse = self.__serveur.accept()
            print(f"[+] Accepté la connection depuis: {addresse[0]}:{addresse[1]}")

            gerant_de_client = threading.Thread(target=self.__gerer_client, args=(client,))
            gerant_de_client.start()


            temps_entre_update = fin - debut

            debut = time.time()
            self.__monde_serveur.mise_a_jour_jeu(temps_entre_update)
            fin = time.time()




