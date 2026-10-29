import constantes
import os
import random
from ursina import *
import __main__ as main
from gestionnaire_langues import GestionnaireLangues

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


def ordonner_boutons(
        boutons: list[Button], 
        d_boutons: float, 
        H_bouton: float, 
        L_bouton: float, 
        debut: float,
        couleur_base = None,
        couleur_survol = None,
        #alpha: float = 0,
        rayon: float = 0
    ) -> list[Button]:
    """
    Ordonne des `ursina.Button` de haut en bas pour un `Menu`
    Args:
        boutons (`list[ursina.Button]`): La liste de boutons à transformer. `boutons[0]` sera en haut
        d_boutons (`float`): La distance entre les boutons
        H_bouton (`float`): La hauteur d'un bouton
        L_bouton (`float`): La largeur d'un bouton
        debut (`float`): La valeur en `y` du premier bouton (`boutons[0]`)
        couleur: La couleur à appliquer à chaque bouton. Si aucune couleur n'est indiquée, aucune valeur de `color` ne sera changée
    Returns:
        Une liste de `ursina.Button` ordonnée
    """

    for idx_b in range(len(boutons)):
        boutons[idx_b].scale = (L_bouton, H_bouton)
        boutons[idx_b].y = debut - idx_b * d_boutons
        boutons[idx_b].text_entity.text = boutons[idx_b].text
        boutons[idx_b].radius = rayon
        #boutons[idx_b].alpha = 0.5



    if couleur_base is not None:
        if couleur_survol is None:
            couleur_survol = couleur_base
        for b in boutons:
            b.color = couleur_base
            b.highlight_color = couleur_survol

    return boutons



