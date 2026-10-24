import constantes
import os
import random

def trouver_dernier_item(d: dict, k: str, s = ".") -> str:
    """
    Args:
        d (dict): Un dictionnaire de dictionnaires
        k (str): La valeur ou branche recherchée
        s (str): Le symbole séparateur
    Returns:
        La valeur à cette branche
    """
    if isinstance(k, str):
        args = k.split(s)
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
                    val = [trouver_dernier_item(item, args[1:]) for item in val]

            return val if len(args) == 1 else trouver_dernier_item(val, args[1:])


def aleatoire_dans_dir(chemin_dir: str, extensions: list[str] = constantes.EXTENSIONS_SON) -> str:
    """
    Args:
        chemin_dir (str): Le chemin vers le directoire visé
        extensions (list[str]): Une liste des extensions à viser
    Returns:
        Un fichier aleatoire ayant une des extensions indiquées
    """
    _dans_dir_cible: list[str] = os.listdir(chemin_dir)
    _fichiers: list[str] = []

    # Ajoute à _fichiers_son seulement les fichier qui ont une des extensions de son permises dans client/constantes.py
    for f in _dans_dir_cible:
        _t: list[str] = f.split('.')

        if _t[-1] in extensions:
            _fichiers.append('.'.join(_t))

    if len(_fichiers) < 1:
        raise Exception("Chemin non existant")

    
    return random.choice(_fichiers)