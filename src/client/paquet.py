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
                None
            )

        _paquet: bytes = tuple_paquet[1]
        print(f"DANS LIRE_PAQUET TYPE EST {_type}")

        if _type < TypePaquetServeur.MAX.value:

            return (
                _type,
                struct.unpack(
                    formats_serveur_par_type[_type.value][1:], # Enleve le char de format
                    _paquet
                )
            )

    except Exception as e:
        print(f"Erreur: le format du paquet n'est pas compatible, paquet: '{_paquet}'")
        print(e)
        exit()


def interpreter_paquet(tuple_paquet: tuple[TypePaquetServeur, tuple[any]]) -> dict[str, any]:
    if tuple_paquet is None: print("PAQUET EST NONe")

    _type: TypePaquetServeur = tuple_paquet[0]

    match _type:
        case TypePaquetServeur.MAJ_JOUEUR:
            print(f"Paquet MAJ JOUEUR: {tuple_paquet}")
            x, y, z, nom, vie, animation = tuple_paquet[1]
            return {
                "Joueur": {
                    "ID": 123,
                    "Position": [x, y, z],
                    "Nom": nom,
                    "En_vie": vie,
                    "Animation": animation
                }
            }

        case TypePaquetServeur.CONNEXION_RATE:
            print("\033[91mErreur de connexion")
            return {
                "Connexion": None
            }

        case TypePaquetServeur.CONNEXION_REUSSIT:
            print("\033[91mConnection réussie")
            return {
                "Connexion": tuple_paquet[1][0]
            }

        case TypePaquetServeur.DECONNEXION:
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
    match b:
        case TypePaquetServeur.MAJ_JOUEUR.value:        
            return struct.calcsize(formats_serveur_par_type[TypePaquetServeur.MAJ_JOUEUR.value]) -1
        case TypePaquetServeur.CONNEXION_REUSSIT.value: 
            return struct.calcsize(formats_serveur_par_type[TypePaquetServeur.CONNEXION_REUSSIT.value]) -1
        case TypePaquetServeur.CONNEXION_RATE.value:    
            return struct.calcsize(formats_serveur_par_type[TypePaquetServeur.CONNEXION_RATE.value]) -1
        case TypePaquetServeur.DECONNEXION.value:       
            return struct.calcsize(formats_serveur_par_type[TypePaquetServeur.DECONNEXION.value]) -1
        case TypePaquetServeur.MAJ_OBSTACLE.value:      
            return struct.calcsize(formats_serveur_par_type[TypePaquetServeur.MAJ_OBSTACLE.value]) -1
        case _ : 
            print(f"IN: {b} AUCUN CASE DE FONCTIONNE")
            exit()
    print(f"BE ES {b}")
    print("QUE PASO AQUI")
 

def deconstruire_superpaquet(superpaquet: list[tuple[TypePaquetServeur, bytes]]) -> dict[str, any]:
    _joueurs: list[dict[str, any]] = []
    _obstacles: list[dict[str, any]] = []
    _connexion: dict[str, any] = {}
    for p in superpaquet:
        _dict_paquet: dict[str, any] = interpreter_paquet(lire_paquet(p))

        if "Joueur" in _dict_paquet:       _joueurs.append(_dict_paquet["Joueur"])
        elif "Obstacle" in _dict_paquet:   _obstacles.append(_dict_paquet["Obstacle"])
        elif "Connexion" in _dict_paquet:  _connexion = _dict_paquet["Connexion"]

    return {
        "Joueurs": _joueurs,
        "Obstacles": _obstacles,
        "Connexion": _connexion
    }