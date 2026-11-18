import socket
import threading
import time
import monde_serveur
import tomllib
from pathlib import Path
import hashlib
import customtkinter as ctk
import variable_globale
import journal
import psutil
import subprocess
import platform
import json

print(str((Path(__file__).parent.parent / 'fermeture_serveur.py')))

class Serveur:
    def __init__(self):
        self.__ouvert = True
        self.__monde_serveur = monde_serveur.MondeServeur()

    def __serveur(self):
        _fichier_toml = open(Path(__file__).parent / "config.toml", 'rb')
        self.__config = tomllib.load(_fichier_toml)
        _serveur: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _serveur.bind((self.__config["Serveur"]["ip"], self.__config["Serveur"]["port"]))
        _serveur.listen(self.__config["Serveur"]["joueurs_max"])

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
        
        while self.__ouvert:
            _client, _addresse = _serveur.accept()
            #_gerant_de_client = threading.Thread(target=self.__gerer_client, args=(_client,_addresse))
            #self.__gerer_client(_client, _addresse)
            #_gerant_de_client.start()
            ### TEST
            _requete = _client.recv(1024)
            
            if _requete == 'fermer'.encode():
                print(_addresse[0])
                print(self.__config["Serveur"]["ip"])
                if _addresse[0] == self.__config["Serveur"]["ip"]:
                    _client.send(b'\x01')
                    _client.close()
                    self.__ouvert = False
                    break

            if _requete == 'ping'.encode():
                _client.send(json.dumps({
                    "nom": self.__config["Info"]["nom"],
                    "description": self.__config["Info"]["description"],
                    "joueurs max": self.__config["Serveur"]["joueurs_max"]
                }).encode())
                _client.close()
                continue

            _dbg_msg = self.__monde_serveur.recevoir_client_paquets(_requete)
            #print(f"Msg {_dbg_msg}")
            _client.send(_dbg_msg)
            
            _client.close()
            ### FIN TEST
            _temps_entre_update = _fin - _debut
            _debut = time.time()
            #self.__monde_serveur.mise_a_jour_jeu()
            #print("MAJ")
            _fin = time.time()

    def __fermer(self, langue, commande):
        self.__destruction(None)

    def __aide(self, langue, commande):
        if langue == 'fr':
            journal.inserer_reponse("fermer ————————————————————————————————————— ferme le serveur")
            journal.inserer_reponse("ajouter-utilisateur <nom> <mot-de-passe> ——— ajoute un utilisateur dans la base de donnée")
            journal.inserer_reponse("connexion-utilisateur <nom> <mot-de-passe> — effectue un test de connexion d'un utilisateur")
            journal.inserer_reponse("retirer-utilisateur <nom> —————————————————— enlève un utilisateur de la base de donnée")
        elif langue == 'en':
            journal.inserer_reponse("exit / stop ———————————————————————— closes the server")
            journal.inserer_reponse("add-user <username> <password> ————— adds a user in the database")
            journal.inserer_reponse("connect-user <username> <password> — does a connection test to a user")
            journal.inserer_reponse("remove-user <nom> —————————————————— removes a user from the database")

    def __ajouter_utilisateur(self, langue, commande):
        if langue == 'fr':
            if self.__monde_serveur.base_donnee.creer_utilisateur(commande[1], hashlib.sha256(hashlib.sha256(commande[2].encode()).digest()).hexdigest()):
                journal.inserer_reponse(f"Utilisateur {commande[1]} a été créé!")
            else:
                journal.inserer_avertissement(f"Un utilisateur avec le même nom éxiste.")
        elif langue == 'en':
            if self.__monde_serveur.base_donnee.creer_utilisateur(commande[1], hashlib.sha256(hashlib.sha256(commande[2].encode()).digest()).hexdigest()):
                journal.inserer_reponse(f"User {commande[1]} has been added!")
            else:
                journal.inserer_avertissement(f"A user with the same username already exists.")

    def __connexion_utilisateur(self, langue, commande):
        if langue == 'fr':
            if self.__monde_serveur.base_donnee.connexion(commande[1], hashlib.sha256(hashlib.sha256(commande[2].encode()).digest()).hexdigest()):
                journal.inserer_reponse(f"Utilisateur {commande[1]} a été connecté!")
            else:
                journal.inserer_avertissement(f"Mauvais nom d'utilisateur ou mot de passe")
        elif langue == 'en':
            if self.__monde_serveur.base_donnee.connexion(commande[1], hashlib.sha256(hashlib.sha256(commande[2].encode()).digest()).hexdigest()):
                journal.inserer_reponse(f"User {commande[1]} has been connected!")
            else:
                journal.inserer_avertissement(f"Wrong username or password.")

    def __retirer_utilisateur(self, langue, commande):
        if langue == 'fr':
            if self.__monde_serveur.base_donnee.retirer(commande[1]):
                journal.inserer_reponse(f"Retiré l'utilisateur « {commande[1]} » !")
            else:
                journal.inserer_reponse(f"n'a pas pu retirer l'utilisateur « {commande[1]} » !")
        if langue == 'en':
            if self.__monde_serveur.base_donnee.retirer(commande[1]):
                journal.inserer_reponse(f"Removed user \"{commande[1]}\" !")
            else:
                journal.inserer_reponse(f"Couldn't remove user \"{commande[1]}\" !")

    def __boucle_principale_sans_graphiques(self, commandes: dict[tuple]):
        time.sleep(0.5)
        while self.__ouvert:
            try:
                _commande = input('❱ ').split(' ')

                journal.inserer_commande(_commande)
        
                if _commande[0] in commandes:
                    commandes[_commande[0]][0](commandes[_commande[0]][1], _commande)
                else:
                    journal.inserer_erreur(f"Commande « {_commande[0]} » n'éxiste pas, écrivez la commande « aide » pour la liste des commandes")
                    journal.inserer_erreur(f"Command \"{_commande[0]}\" doesn't exist, write the command \"help\" for the commands list")
            except KeyboardInterrupt:
                self.__destruction(None)

    def __destruction(self, _):
        # créer une connection pour fermer le programme
        _commande = "py" if platform.system() == "Windows" else "python3"
        subprocess.Popen([_commande, Path(__file__).parent / 'fermeture_serveur.py', self.__config["Serveur"]["ip"], str(self.__config["Serveur"]["port"])])

    def __mettre_a_jour_obstacles(self):
        time.sleep(10)
        while self.__ouvert:
            self.__monde_serveur.effacer_liste_nouveaux_obstacles()
            self.__monde_serveur.nettoyer_tuiles()
            self.__monde_serveur.creer_obstacles()
            #time.sleep(0.01)
            time.sleep(1)

    def __boucle_principale_avec_graphiques(self, commandes: dict[tuple]):
        _fenetre = ctk.CTk()
        _fenetre.title("Ludikrous Makrous")
        _fenetre.resizable(False, False)
        
        _fenetre.bind('<Destroy>', self.__destruction)

        try:

            _conteneur_gauche = ctk.CTkFrame(_fenetre)

            _graphique = ctk.CTkCanvas(_conteneur_gauche, width=300, height=200, bg='white')
            #graphique.grid(row=0, column=0, sticky='n')
            _graphique.pack()

            _graphique_ram = ctk.CTkCanvas(_conteneur_gauche, width=300, height=200, bg='white')
            _graphique_ram.pack()

            _joueurs_texte = ctk.CTkLabel(_conteneur_gauche, text='Joueurs')
            _joueurs_texte.pack()

            _joueurs = ctk.CTkTextbox(_conteneur_gauche, width=300, height=170)
            _joueurs.pack(fill='both')

            #_joueurs.insert(0, "Test1234")

            _conteneur_gauche.grid(row=0,column=0, sticky='n')

            _conteneur_commandes = ctk.CTkFrame(_fenetre)

            _journal = ctk.CTkTextbox(_conteneur_commandes, width=600, height=600, font=("Consolas", 14))
            _journal.pack()

            _journal.tag_config('erreur', foreground="red")
            _journal.tag_config('reponse', foreground="green")
            _journal.tag_config('avertissement', foreground="#E79A0B")

            _conteneur = ctk.CTkFrame(_conteneur_commandes)

            _commande = ctk.CTkEntry(_conteneur, width=510, corner_radius=16, placeholder_text="aide/help")
            _commande.grid(row=0, column=0)

            def _appuyer_commande_e(*args):
                _commande_sep = _commande.get().split(' ')
                journal.inserer_commande(_commande_sep)

                if _commande_sep[0] in commandes:
                    commandes[_commande_sep[0]][0](commandes[_commande_sep[0]][1], _commande_sep)
                else:
                    journal.inserer_erreur(f"Commande « {_commande_sep[0]} » n'éxiste pas, écrivez la commande « aide » pour la liste des commandes")
                    journal.inserer_erreur(f"Command \"{_commande_sep[0]}\" doesn't exist, write the command \"help\" for the commands list")

            _fenetre.bind("<Return>", _appuyer_commande_e)

            _appuyer_commande = ctk.CTkButton(_conteneur, width=70, text="Envoyer", command=_appuyer_commande_e, fg_color='gray', hover_color='dark gray', corner_radius=16)
            _appuyer_commande.grid(row=0, column=1)

            _conteneur.pack()

            _conteneur_commandes.grid(row=0, column=1)

        except Exception as e:
            journal.inserer_erreur("Échec lors de la création de l'interface graphique.")
            journal.inserer_erreur(f"{repr(e)}")
            self.__destruction(None)

        _ancien = time.time()
        donnee_brutes = []
        donnee_brutes_ram = []

        _fait = []

        while self.__ouvert:
            try:
                journal.obtenir_texte(_journal)

                _maintenant = time.time()

                if _maintenant - _ancien > 0.5:
                    _ancien = _maintenant
                    donnee_brutes.append(psutil.cpu_percent())
                    donnee_brutes = donnee_brutes[-20:]
                    _graphique.create_rectangle(0,0,300,200, fill='white', width=0)
                    _graphique.create_line(0, 50, 300, 50, fill='light gray')
                    _graphique.create_line(0, 100, 300, 100, fill='light gray')
                    _graphique.create_line(0, 150, 300, 150, fill='light gray')
                    _graphique.create_text(150, 10, text="Utilisation CPU (%.1f%%)" % (donnee_brutes[len(donnee_brutes)-1],), fill='black')
                    for i, d in enumerate(donnee_brutes):
                        if i > 0:
                            _graphique.create_line(i*(300/20), 200-(d*2), (i-1)*(300/20), 200-(donnee_brutes[i-1]*2), fill='green', width=3)

                    donnee_brutes_ram.append(psutil.virtual_memory().percent)
                    donnee_brutes_ram = donnee_brutes_ram[-20:]

                    _graphique_ram.create_rectangle(0,0,300,200, fill='white', width=0)
                    _graphique_ram.create_line(0, 50, 300, 50, fill='light gray')
                    _graphique_ram.create_line(0, 100, 300, 100, fill='light gray')
                    _graphique_ram.create_line(0, 150, 300, 150, fill='light gray')
                    
                    _graphique_ram.create_text(150, 10, fill='black', text="Utilisation RAM (%.1f/%.1f GB)" % (psutil.virtual_memory().used / 1024 / 1024 / 1024, psutil.virtual_memory().total / 1024 / 1024 / 1024))
                    for i, d in enumerate(donnee_brutes_ram):
                                    if i > 0:
                                        _graphique_ram.create_line(i*(300/20), 200-(d*2), (i-1)*(300/20), 200-(donnee_brutes_ram[i-1]*2), fill='blue', width=3)
                    _joueurs.delete('1.0', "end")
                    for _ in self.__monde_serveur.joueurs():
                        _joueurs.insert('end', _ + '\n')
                    #_joueurs.update()
                _fenetre.update()
            except KeyboardInterrupt:
                self.__destruction(None)
            except Exception as e:
                print(e)

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
            "connect-user": (self.__connexion_utilisateur, "en"),
            "retirer-utilisateur": (self.__retirer_utilisateur, "fr"),
            "remove-user": (self.__retirer_utilisateur, "en")
        }

        _serveur = threading.Thread(target=self.__serveur)
        _serveur.start()

        _obstacles = threading.Thread(target=self.__mettre_a_jour_obstacles)
        _obstacles.start()

        if not variable_globale.interface_graphique:
            self.__boucle_principale_sans_graphiques(_commandes)
        else:
            self.__boucle_principale_avec_graphiques(_commandes)
        _serveur.join()
        _obstacles.join()