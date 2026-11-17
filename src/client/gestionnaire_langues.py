import tomllib
import sqlite3
from config import Config

class GestionnaireLangues:
    liste = ["fr", "en", "es"]
    LANGUE = "fr"
    LANGUE_AVANT = "fr"
    __CHEMIN_DB = "ressources/langages/lang.db"

    @staticmethod
    def obtenir(k: str, lang: str = "fr", db: bool = True) -> str:
        from utilitaires import trouver_dernier_item
        """
        Args:
            k: La clef vers la phrase recherchée
            lang: La langue de la phrase recherchée
        Returns:
            str: La phrase recherchée selon la langue indiquée
        """

        if not db:
            CHEMIN_LANGAGES = "ressources/langages/"

            _chemin_lang = CHEMIN_LANGAGES + GestionnaireLangues.__lang_comme_code(lang) + ".toml"

            with open(_chemin_lang, 'rb') as _fichier_toml:
                _toml_lang: dict = tomllib.load(_fichier_toml)
            #_fichier_toml.close()

            return trouver_dernier_item(_toml_lang, k)

        else:
            return GestionnaireLangues.__obtenir_de_db(k, lang)


    @staticmethod
    def __lang_comme_code(lang: str) -> str:
        _code_lang = ""
        match lang:
            case "fr": _code_lang = "fr_CA"
            case "en": _code_lang = "en_US"
            case "es": _code_lang = "es_419"
            case _   : raise Exception("Code de langue non valide")

        return _code_lang


    @staticmethod
    def __code_comme_lang(code: str) -> str:
        _lang = ""
        match code:
            case "fr_CA": _lang = "fr"
            case "en_US": _lang = "en"
            case "es_419": _lang = "es"
            case _: raise Exception("Code de langue non valide")

        return _lang



    @staticmethod
    def __obtenir_de_db(k: str, lang: str):
        with sqlite3.connect(GestionnaireLangues.__CHEMIN_DB) as _connection_db:
            _curseur = _connection_db.cursor()
            _colonne = GestionnaireLangues.__lang_comme_code(lang).replace('_', '-')

            _curseur.execute(f"SELECT [{_colonne}] FROM lang WHERE clef = '{k}'")

            return _curseur.fetchone()[0]


    @staticmethod
    def trouver_clef(s: str) -> str:
        with sqlite3.connect(GestionnaireLangues.__CHEMIN_DB) as _connection_db:
            _curseur  = _connection_db.cursor()
            _colonne = GestionnaireLangues.__lang_comme_code(GestionnaireLangues.LANGUE).replace('_', '-')
            _sql = f"SELECT clef FROM lang WHERE [{_colonne}] = '{s}'"
            _curseur.execute(_sql)

            return _curseur.fetchone()[0]


    @staticmethod
    def clef_maintenant(s: str) -> str:
        return GestionnaireLangues.trouver_clef(GestionnaireLangues.LANGUE)


    @staticmethod
    def clef_avant(s: str) -> str:
        return GestionnaireLangues.trouver_clef(GestionnaireLangues.LANGUE_AVANT)


    @staticmethod
    def changer(nouvelle_langue: str):
        GestionnaireLangues.LANGUE_AVANT = GestionnaireLangues.LANGUE
        GestionnaireLangues.LANGUE = nouvelle_langue
        _json = Config.json()
        _json["Client"]["langue"] = nouvelle_langue
        Config.modifier(_json)
        
        #print("nuova lingua " + nouvelle_langue)


    @staticmethod
    def de_config():
        """
        Définit la langue en se basant sur la configuration dans `config.json`
        """
        _nouvelle = Config.json()["Client"]["langue"]
        GestionnaireLangues.changer(_nouvelle)