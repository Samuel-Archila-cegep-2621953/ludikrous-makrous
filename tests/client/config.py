import json
import os

class Config:
    CHEMIN: str = "config.json"

    """
    @staticmethod
    def lire_specifique(k: str) -> str:
        with open(Config.CHEMIN, 'r') as _f_json:
            return json.load(_f_json)[k]
    """

    @staticmethod
    def json() -> dict:
        with open(Config.CHEMIN, 'r') as _f_json:
            return json.load(_f_json)

    @staticmethod
    def modifier(j: dict):
        #from utilitaires import trouver_dernier_item
        #with open(Config.CHEMIN, 'r') as _f_json:
        #    _json = json.load(_f_json)

            
        #    try:
        #        _s = trouver_dernier_item(_json, k)
        #    except:
        #        return
        #    _nouveau = json.dumps(_json)

        os.remove(Config.CHEMIN)
        with open(Config.CHEMIN, 'w') as _f_json_temp:
            json.dump(j, _f_json_temp, indent=3)
            _f_json_temp.flush()

        #with  open(Config.CHEMIN, 'w') as _vrai_json:


    @staticmethod
    def changer_nom_affichage(nom: str):
        _cfg = Config.json()
        _cfg["Client"]["nom_affichage"] = nom
        Config.modifier(_cfg)


    @staticmethod
    def changer_ip(ip: str):
        _cfg = Config.json()
        _cfg["Client"]["ip"] = ip
        Config.modifier(_cfg)


    @staticmethod
    def changer_port(port: int):
        _cfg = Config.json()
        _cfg["Client"]["port"] = port
        Config.modifier(_cfg)


    @staticmethod
    def changer_nom_utilisateur(nom: int):
        _cfg = Config.json()
        _cfg["Client"]["nom_utilisateur"] = nom
        Config.modifier(_cfg)


    @staticmethod
    def changer_mdp(mdp: int):
        _cfg = Config.json()
        _cfg["Client"]["mot_de_passe_hache"] = mdp
        Config.modifier(_cfg)