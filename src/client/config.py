import json
import os

class Config:
    CHEMIN: str = "config.json"

    @staticmethod
    def lire(k: str) -> str:
        with open(Config.CHEMIN, 'r') as _f_json:
            return json.loads(_f_json)[k]

    @staticmethod
    def modifier(k: str, val):
        with open(Config.CHEMIN, 'r') as _f_json:
            _json = json.load(_f_json)
            _json[k] = val
            _nouveau = json.dumps(_json)

        os.remove(Config.CHEMIN)
        with open(Config.CHEMIN) as _f_json:
            json.dump(_json, _f_json, indent=3)


            
