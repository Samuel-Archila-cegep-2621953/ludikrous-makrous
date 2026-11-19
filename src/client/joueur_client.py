from prefabs.controlleur_premiere_personne import ControlleurPremierePersonne
from ursina.prefabs.health_bar import HealthBar
import client_serveur
import time
import joueur
from ursina import *
import __main__ as principale
from types_musique import TypesMusique
from musique import Musique
import paquet as Pq
import struct
from type_paquet import *
from config import Config
from math import isnan as is_nan
from debogage import Debogage as Dbg
from monde import Monde
from type_obstacle import TypeObstacle as TyOb
import pilier
from gestionnaire_langues import GestionnaireLangues as Gl
#from obstacles import pilier
from obstacles.missile import Missile

class JoueurClient(ControlleurPremierePersonne):
    def __init__(self, client: client_serveur.Client, monde: Monde, height=2, **kwargs):
        super().__init__(height, **kwargs)
        self.__client = client
        self.__id, self.__session = self.__creer_id()
        self.__dernier_temps = self.__obtenir_temps()
        self.__joueurs: list[joueur.Joueur] = []
        self.vie = HealthBar(
            parent=camera.ui,
            bar_color=rgb(84/255, 23/255, 14/255),
            roundness=0,
            value=255,
            max_value=255,
            y=0.45,
            x= -0.8,
            color=rgb(129/255,129/255,129/255),
            scale=(0.3, 0.05),
            show_text=False
        )
        self.vie_logo = Entity(
            parent=camera.ui,
            texture='ressources/textures/hud/vie',
            y=0.425,
            x=-0.83,
            scale=(0.05, 0.05),
            model='quad'
        )
        self.pointeur = Entity(
            parent=camera.ui,
            texture='ressources/textures/hud/pointeur',
            y=0,
            x=0,
            scale=(0.02, 0.02),
            model='quad'
        )
        self.spectateur = Text(Gl.obtenir("jeu.texte.spectateur", Gl.LANGUE), origin=(0,0.5), scale=(2,2), y = 0.5)
        self.spectateur.visible_setter(False)
        self.cursor.visible = False

        self.musique = Musique(TypesMusique.JEU_FACILE)
        self.musique.fade_in(0.7)

        self.monde = monde

        self.__obstacles = []

    def __creer_id(self) -> int:
        """
        _resultat = self.__client.envoyer_message(json.dumps({
                "Type": "CREER ID"
            }))
        _donnee = json.loads(_resultat)
        """

        #_mdp_hache = Config.json()["Client"]["mot_de_passe_hache"].encode("ascii")
        _mdp_hache = bytes.fromhex(Config.json()["Client"]["mot_de_passe_hache"].strip())
        _nom_utilisateur = Config.json()["Client"]["nom_utilisateur"].encode("ascii")
        Dbg.info(_mdp_hache, 3)

        _donnee = self.__client.envoyer_message(struct.pack(
            formats_clients_par_type[TypePaquetClient.CONNEXION.value],
            TypePaquetClient.CONNEXION.value,
            _nom_utilisateur,
            _mdp_hache)
        )
        _hache = _donnee["Session"]

        Dbg.info(f"[+] Hache obtenue comme ID: {_hache}", 3)
        #return _donnee['ID']
        if _hache == None: exit(1)
        return (_donnee['Connexion'], _hache)

    def __obtenir_temps(self) -> float:
        return time.time()

    def __emballer_les_donnees(self) -> bytes:
        """
        return json.dumps({
            "Type": "MAJ",
            "ID": self.__id,
            "Position": [
                self.position.x,
                self.position.y,
                self.position.z
            ]
        })
        """
        #TODO! Convertir en struct
        return struct.pack(
                formats_clients_par_type[TypePaquetClient.MAJ_JOUEUR.value], # FORMAT
                #NOTE VIEUX TypePaquetClient.MAJ_JOUEUR.value[0],
                TypePaquetClient.MAJ_JOUEUR.value,                            # TYPE
                #NOTE VIEUX Config.json()["Client"]["mot_de_passe_hache"].encode("ascii"),
                self.__session, # hache clé
                floor(self.position.x * 100),
                floor(self.position.y * 100),
                floor(self.position.z * 100),
                self.vie.value,
                3 # TODO Animations
            )

    def joueurs(self) -> list[joueur.Joueur]:
        return self.__joueurs

    def lire_donnee(self, donnee_texte: dict):
        #NOTE VEUX_donnee = json.loads(donnee_texte)
        _donnee = donnee_texte
        Dbg.info("DONNEES LUES", 5)

        _joueurs = _donnee["Joueurs"]
        for i, _ in enumerate(_joueurs):
            _position: list[float] = _['Position']

            for p_idx, p in enumerate(_position):
                if is_nan(p):
                    Dbg.err(f"ERREUR0: Position d'un joueur est NaN. Position: {_position}")
                    _position[p_idx] = 0.0

            if i >= len(self.__joueurs):
                _joueur = joueur.Joueur(_joueurs[i]["ID"], '', (_position[0], _position[1], _position[2]))
                print(_joueurs[i]["ID"], self.__id)
                if _joueurs[i]["ID"] == self.__id:
                    _joueur.visible_setter(False)
                self.__joueurs.append(_joueur)

            #else:
            elif _["ID"] != self.__id:  # Ne pas se mettre à jour soi-même?
                _pos = (_position[0] / 100, _position[1] / 100, _position[2] / 100)
                Dbg.info(_pos, 4)
                for p_idx, p in enumerate(_pos):
                    if is_nan(p):
                        Dbg.err(f"ERREUR1: Position d'un joueur est NaN. Position: {_position}")
                        _position[p_idx] = 0.0
                        Dbg.err(f"Position corrigée: {_pos}")
                self.__joueurs[i].position = _pos

        for jq in _donnee['Joueurs quittés']:
            destroy(self.__joueurs[jq])
            del self.__joueurs[jq]

        _obstacles: list[dict] = _donnee["Obstacles"]

        for j, obs in enumerate(_obstacles):
            try:
                match obs["Type"]:
                    case TyOb.MISSILE.value:
                        _missile = Missile(obs["Coord"], self)
                        self.__obstacles.append(_missile)
                    case TyOb.PILIER.value:
                        _coord: tuple[int, int] = obs["Coord"]
                        _hauteur = pilier.Pilier.hauteur_depuis_mode(obs["Hauteur"])
                        self.monde.changer_hauteur_tuile(_coord[0], _coord[1], _hauteur)
            except Exception as e:
                Dbg.err("JoueurClient::lire_donnee::Branche(obstacles): Erreur", 2)
                Dbg.err(e)


    def __remettre_en_vie(self):
        self.mode_camera = 'mouvement'
        self.position = (16, 15, 16)
        self.spectateur.visible_setter(False)

    def update(self):
        super().update()
        temps_en_ce_moment = self.__obtenir_temps()
        if temps_en_ce_moment - self.__dernier_temps > 1 / 12:
            #NOTE VIEUX self.lire_donnee(Pq.interpreter_paquet(self.__client.envoyer_message(self.__emballer_les_donnees())), TypePaquetServeur.MAJ_JOUEUR)
            self.lire_donnee(self.__client.envoyer_message(self.__emballer_les_donnees()))

        if self.vie.value <= 0:
            self.vie.value = 255
            self.spectateur.visible_setter(True)
            self.mode_camera = 'mort'
            invoke(self.__remettre_en_vie, delay=5)

        #print(self.position)
        if self.position.y < -10:
            self.velocite_verticale = 0
            self.position = (16, 15, 16)
            #self.vie.value //= 2
            self.vie.value -= 128



    def reduire_vie(self, quantite: float):
        self.vie.value -= quantite

    def __emballer_deconnexion(self) -> bytes:
        return struct.pack(
            formats_clients_par_type[TypePaquetClient.DECONNEXION.value],
            TypePaquetClient.DECONNEXION.value,
            self.__session
        )

    def input(self,key):
        super().input(key)
        match key:
            case "escape":
                self.__client.envoyer_message(self.__emballer_deconnexion())
                principale.terminer_jeu()
            case "-": self.reduire_vie(3)
            case "=": self.vie.value += 10


    def creer_liste_score():
        """
        Reçoit une liste de joueurs des serveurs et crée une list[tuple[str, int]] contenant les noms et scores des joueurs
        """
        # TODO!
        pass
