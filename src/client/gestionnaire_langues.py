import tomllib
import sqlite3

class GestionnaireLangues:
    liste = ["fr", "en", "es"]
    LANGUE = "fr"

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
    def __lang_comme_code(lang: str):
        _code_lang = ""
        match lang:
            case "fr": _code_lang = "fr_CA"
            case "en": _code_lang = "en_US"
            case "es": _code_lang = "es_419"
            case _: raise Exception("Code de langue non valide")

        return _code_lang


    @staticmethod
    def __obtenir_de_db(k: str, lang: str):
        with sqlite3.connect("ressources/langages/lang.db") as _connection_db:
            _curseur = _connection_db.cursor()
            _colonne = GestionnaireLangues.__lang_comme_code(lang).replace('_', '-')

            _curseur.execute(f"SELECT [{_colonne}] FROM lang WHERE clef = '{k}'")

            return _curseur.fetchone()[0]