import tomllib
from utilitaires import trouver_dernier_item

class GestionnaireLangues:
    @staticmethod
    def obtenir(k: str, lang: str) -> str:
        """
        Args:
            k: La clef vers la phrase recherchée
            lang: La langue de la phrase recherchée
        Returns:
            str: La phrase recherchée selon la langue indiquée
        """
        
        CHEMIN_LANGAGES = "ressources/langages"

        _prefixe_langage = ""
        _parent = "ressources/langages/"

        match lang:
            case "fr": _prefixe_langage = "fr_CA"
            case "en": _prefixe_langage = "en_US"
            case "es": _prefixe_langage = "es_419"

        _chemin_lang = _parent + _prefixe_langage + ".toml"
        _fichier_toml = open(_chemin_lang, 'rb')
        _toml_lang: dict = tomllib.load(_fichier_toml)

        return trouver_dernier_item(_toml_lang, k)

