import socket
import threading
import time
import monde_serveur
import tomllib
from pathlib import Path
import select

class Serveur:
    def __init__(self):
        self.__ouvert = True
        self.__monde_serveur = monde_serveur.MondeServeur()

    def __gerer_client(self, socket_client: socket.socket):
        _requete = socket_client.recv(1024)
        # print(f"[+] Reçu: {_requete}")

        socket_client.send(self.__monde_serveur.recevoir_client_paquets(_requete))

        socket_client.close()

    def __serveur(self):
        _fichier_toml = open(Path(__file__).parent / "config.toml", 'rb')
        self.__config = tomllib.load(_fichier_toml)
        _serveur: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _serveur.bind((self.__config["Serveur"]["ip"], self.__config["Serveur"]["port"]))
        _serveur.listen(5)
        print(f"Serveur lancé sur {self.__config["Serveur"]["ip"]}:{self.__config["Serveur"]["port"]}")

        _temps_entre_update = 0.0
        _debut = 0.0
        _fin = 0.0

        entrees = [_serveur]
        sorties = []
        
        while self.__ouvert:
            _lisable, _ecrivable, _exceptionelles = select.select(entrees, sorties, entrees, 1)
            for s in _lisable:
                if s is _serveur:
                    _client, _addresse = s.accept()
                    _client.setblocking(0)
                    entrees.append(_client)
                    _gerant_de_client = threading.Thread(target=self.__gerer_client, args=(_client,))
                    _gerant_de_client.start()
                
                
                    _temps_entre_update = _fin - _debut
                
                    _debut = time.time()
                    self.__monde_serveur.mise_a_jour_jeu(_temps_entre_update)
                    _fin = time.time()

    def __fermer(self, langue):
        self.__ouvert = False

    def __aide(self, langue):
        if langue == 'fr':
            print("fermer — ferme le serveur")
        elif langue == 'en':
            print("exit / stop — closes the server")

    def boucle_principale(self):
        _commandes = {
            "fermer": (self.__fermer, "fr"),
            "exit": (self.__fermer, "en"),
            "stop": (self.__fermer, "en"),
            "aide": (self.__aide, "fr"),
            "help": (self.__aide, "en")
        }

        _serveur = threading.Thread(target=self.__serveur)
        _serveur.start()
        time.sleep(0.5)
        while self.__ouvert:
            _commande = input('> ')
            if _commande in _commandes:
                _commandes[_commande][0](_commandes[_commande][1])
            else:
                print(f"Commande « {_commande} » n'éxiste pas, écrivez la commande « aide » pour la liste des commandes")
                print(f"Command \"{_commande}\" doesn't exist, write the command \"help\" for the commands list")

        _serveur.join()




