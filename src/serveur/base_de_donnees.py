import sqlite3
from pathlib import Path
from debogage import Debogage as Dbg

class BaseDeDonnees:
    def __init__(self):
        # bd = base de donnée
        #self.__bd = sqlite3.connect(Path(__file__).parent / "serveur.db")
        # BUG: sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread. The object was created in thread id 25840 and this is thread id 8524.
        # UNSAFE FIX  ?
        self.__bd = sqlite3.connect(Path(__file__).parent / "serveur.db", check_same_thread = False)
        self.__curseur = self.__bd.cursor()

        self.__curseur.execute("""
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pseudonyme TEXT UNIQUE NOT NULL,
            mot_de_passe TEXT NOT NULL,
            date_creation TEXT DEFAULT (datetime('now', 'localtime'))
        )
        """)
        self.__bd.commit()

    def creer_utilisateur(self, nom: str, mot_de_passe_hache: str) -> bool:
        """
        Crée un utilisateur dans la base de donnée
        Args:
            nom (str): le pseudonyme du joueur
            mot_de_passe_hache (str): le mot-de-passe haché
        Returns:
            bool: réussite; réussit = True, raté = False
        """
        if not self.__verifier_personne_existe(nom):
            self.__curseur.execute("INSERT INTO utilisateurs (pseudonyme, mot_de_passe) VALUES (?, ?)", (nom, mot_de_passe_hache))
            self.__bd.commit()
            return True
        return False

    def __verifier_personne_existe(self, nom: str) -> bool:
        self.__curseur.execute("SELECT id FROM utilisateurs WHERE pseudonyme = ?", (nom,))
        _resultat = self.__curseur.fetchone()
        Dbg.info(f"Résultat de __verifier_personne_existe: {_resultat != None} ", 2)
        return _resultat != None

    def obtenir_id(self, nom: str) -> int:
        self.__curseur.execute("SELECT id FROM utilisateurs WHERE pseudonyme = ?", (nom,))
        _resultat = self.__curseur.fetchone()
        return _resultat

    def connexion(self, nom: str, mot_de_passe_hache: str) -> bool:
        """
        Connecter l'utilisateur à partir de son pseudonyme et de son mot de passe.
        Args:
            nom (str): pseudonyme
            mot_de_passe_hache (str): mot-de-passe haché
        Returns:
            bool: réussite; réussit = True, raté = False
        """
        if self.__verifier_personne_existe(nom):
            self.__curseur.execute("SELECT mot_de_passe FROM utilisateurs WHERE pseudonyme = ?", (nom,))
            _resultat = self.__curseur.fetchone()

            if mot_de_passe_hache != _resultat[0]:
                Dbg.err(
                    f"""MDP:      '{mot_de_passe_hache}' / {len(mot_de_passe_hache)}
                    Expected: '{_resultat[0]}' / {len(_resultat[0])}""",
                    2
                )

            return mot_de_passe_hache == _resultat[0]

        # NOTE Test de la class Debogage
        Dbg.err(f"PERSONNE {nom} N'EXISTE PAS", 2)

        return False

    def retirer(self, nom: str) -> bool:
        """
        Retirer l'utilisateur à partir de son pseudonyme.
        Args:
            nom (str): pseudonyme
        Returns:
            bool: réussite; réussit = True, raté = False
        """
        if self.__verifier_personne_existe(nom):
            self.__curseur.execute("DELETE FROM utilisateurs WHERE pseudonyme = ?", (nom,))
            self.__bd.commit()
            return True
        return False

    def __del__(self):
        self.__bd.close()