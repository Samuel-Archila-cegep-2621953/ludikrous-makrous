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
        _parent = "ressources/langages/"

        match lang:
            case "fr": _prefixe_langage = "fr_CA"
            case "en": _prefixe_langage = "en_US"
            case "es": _prefixe_langage = "es_419"

        _chemin_lang = _parent + _prefixe_langage + ".toml"
        _fichier_toml = open(_chemin_lang, 'rb')
        _toml_lang: dict = tomllib.load(_fichier_toml)

        def __trouver_dernier_item(d: dict, k: str) -> str:
            if isinstance(k, str):
                args = k.split('.')
            else:
                args = k

            if args and d:
                element = args[0]
                if element:
                    if isinstance(d, list):
                        vals = []
                        val = [m for m in d if m is not None]
                        if any(isinstance(i, list) for i in val):
                            for l in val:
                                if isinstance(l, list):
                                    vals += [v for v in l if v is not None]
                        else:
                            vals += [v for v in val if not isinstance(v, list)]
                        val = vals

                    else:
                        val = d.get(element)

                    if isinstance(val, list):
                        if len(val) > 0 and isinstance(val[0], dict):
                            val = [__trouver_dernier_item(item, args[1:]) for item in val]

                    return val if len(args) == 1 else __trouver_dernier_item(val, args[1:])

        return __trouver_dernier_item(_toml_lang, k)

