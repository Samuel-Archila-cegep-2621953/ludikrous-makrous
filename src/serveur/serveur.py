import socket
import threading
import time
import monde_serveur
import tomllib
from pathlib import Path
import select
import hashlib
import tkinter as tk
import tkinter.ttk as ttk
import variable_globale
import journal
import psutil

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

        print(""" █████                      █████  ███  █████                                                                         █████                                           
░░███                      ░░███  ░░░  ░░███                                                                         ░░███                                            
 ░███        █████ ████  ███████  ████  ░███ █████ ████████   ██████  █████ ████  █████     █████████████    ██████   ░███ █████ ████████   ██████  █████ ████  █████ 
 ░███       ░░███ ░███  ███░░███ ░░███  ░███░░███ ░░███░░███ ███░░███░░███ ░███  ███░░     ░░███░░███░░███  ░░░░░███  ░███░░███ ░░███░░███ ███░░███░░███ ░███  ███░░  
 ░███        ░███ ░███ ░███ ░███  ░███  ░██████░   ░███ ░░░ ░███ ░███ ░███ ░███ ░░█████     ░███ ░███ ░███   ███████  ░██████░   ░███ ░░░ ░███ ░███ ░███ ░███ ░░█████ 
 ░███      █ ░███ ░███ ░███ ░███  ░███  ░███░░███  ░███     ░███ ░███ ░███ ░███  ░░░░███    ░███ ░███ ░███  ███░░███  ░███░░███  ░███     ░███ ░███ ░███ ░███  ░░░░███
 ███████████ ░░████████░░████████ █████ ████ █████ █████    ░░██████  ░░████████ ██████     █████░███ █████░░████████ ████ █████ █████    ░░██████  ░░████████ ██████ 
░░░░░░░░░░░   ░░░░░░░░  ░░░░░░░░ ░░░░░ ░░░░ ░░░░░ ░░░░░      ░░░░░░    ░░░░░░░░ ░░░░░░     ░░░░░ ░░░ ░░░░░  ░░░░░░░░ ░░░░ ░░░░░ ░░░░░      ░░░░░░    ░░░░░░░░ ░░░░░░  
                                                                ▄▀▀▀ ▄▄  ▄ ▄▄ ▄   ▄  ▄▄  ▄  ▄ ▄ ▄▄ 
                                                                ▀▀▄ █▀▀▀ █▀   ▀▄ ▄▀ █▀▀▀ █  █ █▀   
                                                                ▀▀▀  ▀▀▀ ▀      ▀    ▀▀▀  ▀▀▀ ▀    
                                                                            """)

        journal.inserer_info(f"Serveur lancé sur {self.__config["Serveur"]["ip"]}:{self.__config["Serveur"]["port"]}")

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
            journal.inserer_reponse("fermer ————————————————————————————————————— ferme le serveur")
            journal.inserer_reponse("ajouter-utilisateur <nom> <mot-de-passe> ——— ajoute un utilisateur dans la base de donnée")
            journal.inserer_reponse("connexion-utilisateur <nom> <mot-de-passe> — effectue un test de connexion d'un utilisateur")
        elif langue == 'en':
            journal.inserer_reponse("exit / stop ———————————————————————— closes the server")
            journal.inserer_reponse("add-user <username> <password> ————— adds a user in the database")
            journal.inserer_reponse("connect-user <username> <password> — does a connection test to a user")

    def __ajouter_utilisateur(self, langue, commande):
        if langue == 'fr':
            if self.__monde_serveur.base_donnee.creer_utilisateur(commande[1], hashlib.sha256(hashlib.sha256(commande[2].encode()).digest()).hexdigest()):
                journal.inserer_reponse(f"Utilisateur {commande[1]} a été créé!")
            else:
                journal.inserer_erreur(f"Un utilisateur avec le même nom éxiste.")
        elif langue == 'en':
            if self.__monde_serveur.base_donnee.creer_utilisateur(commande[1], hashlib.sha256(hashlib.sha256(commande[2].encode()).digest()).hexdigest()):
                journal.inserer_reponse(f"User {commande[1]} has been added!")
            else:
                journal.inserer_erreur(f"A user with the same username already exists.")

    def __connexion_utilisateur(self, langue, commande):
        if langue == 'fr':
            if self.__monde_serveur.base_donnee.connexion(commande[1], hashlib.sha256(hashlib.sha256(commande[2].encode()).digest()).hexdigest()):
                journal.inserer_reponse(f"Utilisateur {commande[1]} a été connecté!")
            else:
                journal.inserer_erreur(f"Mauvais nom d'utilisateur ou mot de passe")
        elif langue == 'en':
            if self.__monde_serveur.base_donnee.connexion(commande[1], hashlib.sha256(hashlib.sha256(commande[2].encode()).digest()).hexdigest()):
                journal.inserer_reponse(f"User {commande[1]} has been connected!")
            else:
                journal.inserer_erreur(f"Wrong username or password.")

    def __boucle_principale_sans_graphiques(self, commandes: dict[tuple]):
        time.sleep(0.5)
        while self.__ouvert:
            try:
                _commande = input('> ').split(' ')

                journal.inserer_commande(_commande)
        
                if _commande[0] in commandes:
                    commandes[_commande[0]][0](commandes[_commande[0]][1], _commande)
                else:
                    journal.inserer_erreur(f"Commande « {_commande[0]} » n'éxiste pas, écrivez la commande « aide » pour la liste des commandes")
                    journal.inserer_erreur(f"Command \"{_commande[0]}\" doesn't exist, write the command \"help\" for the commands list")
            except KeyboardInterrupt:
                self.__ouvert = False
    def __boucle_principale_avec_graphiques(self, commandes: dict[tuple]):
        _fenetre = tk.Tk()
        _fenetre.title("Ludikrous Makrous")

        def _destruction(_):
            self.__ouvert = False
        
        _fenetre.bind('<Destroy>', _destruction)

        try:

            _graphique = tk.Canvas(_fenetre, width=300, height=200, bg='black')
            _graphique.grid(row=0, column=0, sticky='n')

            _conteneur_commandes = ttk.Frame(_fenetre)

            _journal = tk.Text(_conteneur_commandes, width=60, height=40)
            _journal.pack()

            _conteneur = ttk.Frame(_conteneur_commandes)

            _commande = ttk.Entry(_conteneur, width=55)
            _commande.grid(row=0, column=0)

            def _appuyer_commande_e():
                _commande_sep = _commande.get().split(' ')
                journal.inserer_commande(_commande_sep)

                if _commande_sep[0] in commandes:
                    commandes[_commande_sep[0]][0](commandes[_commande_sep[0]][1], _commande_sep)
                else:
                    journal.inserer_erreur(f"Commande « {_commande_sep[0]} » n'éxiste pas, écrivez la commande « aide » pour la liste des commandes")
                    journal.inserer_erreur(f"Command \"{_commande_sep[0]}\" doesn't exist, write the command \"help\" for the commands list")


            _appuyer_commande = ttk.Button(_conteneur, width=10, text="Envoyer", command=_appuyer_commande_e)
            _appuyer_commande.grid(row=0, column=1)

            _conteneur.pack()

            _conteneur_commandes.grid(row=0, column=1)
        except:
            journal.inserer_erreur("Échec lors de la création de l'interface graphique.")
            self.__ouvert = False

        _ancien = time.time()
        donnee_brutes = []

        while self.__ouvert:
            try:
                _journal.insert(tk.END, journal.obtenir_texte())

                _maintenant = time.time()

                if _maintenant - _ancien > 0.1:
                    _ancien = _maintenant
                    donnee_brutes.append(psutil.cpu_percent())
                    donnee_brutes = donnee_brutes[-80:]
                    _graphique.create_rectangle(0,0,300,200, fill='black')
                    for i, d in enumerate(donnee_brutes):
                        _graphique.create_rectangle(i*(300/80), 200-(d*2), i*(300/80)+3, 200-(d*2+3), fill='white', width=2)

                _fenetre.update()
            except KeyboardInterrupt:
                self.__ouvert = False

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

        if not variable_globale.interface_graphique:
            self.__boucle_principale_sans_graphiques(_commandes)
        else:
            self.__boucle_principale_avec_graphiques(_commandes)
        _serveur.join()