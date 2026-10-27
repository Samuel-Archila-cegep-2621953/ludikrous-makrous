import json
import os

class Config:
    CHEMIN: str = "config.json"

    @staticmethod
    def lire_specifique(k: str) -> str:
        with open(Config.CHEMIN, 'r') as _f_json:
            return json.load(_f_json)[k]

    @staticmethod
    def json() -> str:
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
        with open(Config.CHEMIN, 'w') as _f_json:
            json.dump(j, _f_json, indent=3)


    @staticmethod
    def changer_nom(nom: str):
        _cfg = Config.json()
        _cfg["Client"]["nom_affichage"] = nom
        Config.modifier(_cfg)



            
