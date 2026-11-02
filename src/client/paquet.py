import struct
from type_paquet import *


def lire_paquet(tuple_paquet: tuple[TypePaquetServeur, bytes]) -> tuple[TypePaquetServeur, tuple[any]]:
    """
    Lit un paquet et l'exporte en tuple.
    """
    print(f"LEN PAQUET {len(tuple_paquet)}")
    try:
        _type: TypePaquetServeur = tuple_paquet[0]
        if _type == TypePaquetServeur.CONNEXION_RATE:
            return (
                _type,
                "Ratee"
            )
        elif _type == TypePaquetServeur.DECONNEXION:
            return (
                _type,
                "Deconnexion"
            )

        _paquet: bytes = tuple_paquet[1]
        print(f"DANS LIRE_PAQUET TYPE EST {_type}")

        if _type.value <= TypePaquetServeur.max():
            _format = formats_serveur_par_type[_type.value][1:] # Enleve le char de format
            print(f"DANS LIRE_PAQUET FORMAT EST {_format}, d'une longueur de {struct.calcsize(_format)},\n len paquet est {len(_paquet)}")

            return (
                _type,
                struct.unpack(
                    _format,
                    _paquet # Le paquet n'inclue pas le u8 de format au début
                )
            )

    except Exception as e:
        print("Dans paquet.lire_paquet():")
        print(f"Erreur: le format du paquet n'est pas compatible, paquet: '{_paquet}'")
        print(f"Len paquet: {len(_paquet)}")
        print(e)
        exit(1)


def interpreter_paquet(tuple_paquet: tuple[TypePaquetServeur, tuple[any]]) -> dict[str, any]:
    if tuple_paquet is None: print("PAQUET EST NONe")

    _type: TypePaquetServeur = tuple_paquet[0]

    match _type:
        case TypePaquetServeur.MAJ_JOUEUR:
            print(f"Paquet MAJ JOUEUR: {tuple_paquet}")
            id, nom, x, y, z, vie, animation = tuple_paquet[1]
            # CHANGE: 2-11-2026. Samuel.
            return {
                "Joueur": {
                    "ID": id,
                    "Position": [x, y, z],
                    "Nom": nom,
                    "En_vie": vie,
                    "Animation": animation
                }
            }

        case TypePaquetServeur.CONNEXION_RATE:
            print("\033[91mErreur de connexion")
            return {
                "Connexion": "Ratee"
            }

        case TypePaquetServeur.CONNEXION_REUSSIT:
            print("\033[91mConnection réussie")
            return {
                "Connexion": tuple_paquet[1][0]
            }

        case TypePaquetServeur.DECONNEXION: # NOTE ASSUMER JOUEUR QUITTES
            print("\033[91mDeconnexion")
            return {
                "Connexion": tuple_paquet[1][0]
            }

        case TypePaquetServeur.MAJ_OBSTACLE:
            type_obstacle, position = tuple_paquet[1]
            return {
                "Obstacle": {
                    "Type": type_obstacle,
                    "Position": position
                }
            }


def longueur_paquet(b: int) -> int:
    """
    Prend 1 byte est retourne la grandeur du message qui le suit selon son type, sans inclure l'en-tête
    """
    # 30-10-2026 >> changé la façon de calculer la taille d'un paquet, en utilisant moins de nests – gardé l'ancien code en cas d'échec.
    # 31-10-2026 >> Changement de MAX pour une fonction, car ça fait un peu plus de sens
    if b > TypePaquetServeur.max():
        print(f"Aucun paquet de ce type. Valeur: {b}.")
        exit(1)

    _longueur = struct.calcsize('>' + formats_serveur_par_type[b]) - 1 # NOTE Samuel: 2-11-2026: Ajout de '>' au format pour que struct.calcsize retourne la valeur correcte en forçant BIG ENDIAN
    #NOTE VIEUX _longueur = struct.calcsize(formats_serveur_par_type[b]) - 1
    print(f"DANS paquet.longueur_paquet: Un paquet de type {b} a une longueur de {_longueur} selon type_paquet.py")
    return _longueur
 

def deconstruire_superpaquet(superpaquet: list[tuple[TypePaquetServeur, bytes]]) -> dict[str, any]:
    _joueurs: list[dict[str, any]] = []
    _joueurs_quittes: list[int] = []
    _obstacles: list[dict[str, any]] = []
    _connexion: dict[str, any] = {}
    for p in superpaquet:
        _dict_paquet: dict[str, any] = interpreter_paquet(lire_paquet(p))

        if "Joueur" in _dict_paquet:       _joueurs.append(_dict_paquet["Joueur"])
        elif "Obstacle" in _dict_paquet:   _obstacles.append(_dict_paquet["Obstacle"])
        elif "Connexion" in _dict_paquet:  _connexion = _dict_paquet["Connexion"]
        elif "Joueurs quittés" in _dict_paquet:  _joueurs_quittes = _dict_paquet["Joueurs quittés"]

    return {
        "Joueurs": _joueurs,
        "Obstacles": _obstacles,
        "Connexion": _connexion,
        "Joueurs quittés": _joueurs_quittes
    }