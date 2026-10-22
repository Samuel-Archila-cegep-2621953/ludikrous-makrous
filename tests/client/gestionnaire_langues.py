import tomllib

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

        match lang:
            case "fr": _prefixe_langage = "fr_CA"
            case "en": _prefixe_langage = "en_US"

        _chemin_lang = _prefixe_langage + ".toml"

        _toml_lang = tomllib.load(_chemin_lang)

        return _toml_lang[k]

