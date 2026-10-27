import socket
import threading
import time
import monde_serveur
import tomllib
from pathlib import Path
import select
import hashlib

class Serveur:
    def __init__(self):
        self.__ouvert = True
        self.__monde_serveur = monde_serveur.MondeServeur()

    def __gerer_client(self, socket_client: socket.socket):
        _requete = socket_client.recv(1024)

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

    def __fermer(self, langue, commande):
        self.__ouvert = False

    def __aide(self, langue, commande):
        if langue == 'fr':
            print("fermer ————————————————————————————————————— ferme le serveur")
            print("ajouter-utilisateur <nom> <mot-de-passe> ——— ajoute un utilisateur dans la base de donnée")
            print("connexion-utilisateur <nom> <mot-de-passe> — effectue un test de connexion d'un utilisateur")
        elif langue == 'en':
            print("exit / stop ———————————————————————— closes the server")
            print("add-user <username> <password> ————— adds a user in the database")
            print("connect-user <username> <password> — does a connection test to a user")

    def __ajouter_utilisateur(self, langue, commande):
        if langue == 'fr':
            if self.__monde_serveur.base_donnee.creer_utilisateur(commande[1], hashlib.sha256(hashlib.sha256(commande[2].encode()).digest()).hexdigest()):
                print(f"Utilisateur {commande[1]} a été créé!")
            else:
                print(f"Un utilisateur avec le même nom éxiste.")
        elif langue == 'en':
            if self.__monde_serveur.base_donnee.creer_utilisateur(commande[1], hashlib.sha256(hashlib.sha256(commande[2].encode()).digest()).hexdigest()):
                print(f"User {commande[1]} has been added!")
            else:
                print(f"A user with the same username already exists.")

    def __connexion_utilisateur(self, langue, commande):
        if langue == 'fr':
            if self.__monde_serveur.base_donnee.connexion(commande[1], hashlib.sha256(hashlib.sha256(commande[2].encode()).digest()).hexdigest()):
                print(f"Utilisateur {commande[1]} a été connecté!")
            else:
                print(f"Mauvais nom d'utilisateur ou mot de passe")
        elif langue == 'en':
            if self.__monde_serveur.base_donnee.connexion(commande[1], hashlib.sha256(hashlib.sha256(commande[2].encode()).digest()).hexdigest()):
                print(f"User {commande[1]} has been connected!")
            else:
                print(f"Wrong username or password.")

    def boucle_principale(self):
        _commandes = {
            "fermer": (self.__fermer, "fr"),
            "exit": (self.__fermer, "en"),
            "stop": (self.__fermer, "en"),
            "aide": (self.__aide, "fr"),
            "help": (self.__aide, "en"),
            "ajouter-utilisateur": (self.__ajouter_utilisateur, "fr"),
            "add-user": (self.__ajouter_utilisateur, "en"),
            "connexion-utilisateur": (self.__connexion_utilisateur, "fr"),
            "connect-user": (self.__connexion_utilisateur, "en")
        }

        _serveur = threading.Thread(target=self.__serveur)
        _serveur.start()
        time.sleep(0.5)
        while self.__ouvert:
            _commande = input('> ').split(' ')

            if _commande[0] in _commandes:
                _commandes[_commande[0]][0](_commandes[_commande[0]][1], _commande)
            else:
                print(f"Commande « {_commande} » n'éxiste pas, écrivez la commande « aide » pour la liste des commandes")
                print(f"Command \"{_commande}\" doesn't exist, write the command \"help\" for the commands list")

        _serveur.join()



