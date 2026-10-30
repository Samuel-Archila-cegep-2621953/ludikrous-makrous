import struct
from type_paquet import *


def lire_paquet(tuple_paquet: tuple[TypePaquetServeur, bytes]) -> tuple[TypePaquetServeur, tuple[any]]:
    """
    Lit un paquet et l'exporte en tuple.
    """
    print(f"LEN PAQUET {len(paquet)}")
    try:
        _type: TypePaquetServeur = tuple_paquet[0]
        if _type == TypePaquetServeur.CONNEXION_RATE:
            return (
                _type,
                None
            )

        _paquet: bytes = tuple_paquet[1]
        print(f"DANS LIRE_PAQUET TYPE EST {_type}")
        #NOTE Vieux if _type < TypePaquetClient.MAX.value:

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


#NOTE VIEUX def interpreter_paquet(paquet: tuple, type: TypePaquetServeur) -> dict:
def interpreter_paquet(tuple_paquet: tuple[TypePaquetServeur, tuple[any]]) -> dict[str, any]:
    if tuple_paquet is None: print("PAQUET EST NONe")

    _type: TypePaquetServeur = tuple_paquet[0]

    #_paquet = if len(paquet) > 0 paquet[1] else None
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
    try:
        match b:
            case TypePaquetServeur.MAJ_JOUEUR.value:        return struct.calcsize(formats_serveur_par_type[TypePaquetServeur.MAJ_JOUEUR.value]) -1
            case TypePaquetServeur.CONNEXION_REUSSIT.value: return struct.calcsize(formats_serveur_par_type[TypePaquetServeur.CONNEXION_REUSSIT.value]) -1
            case TypePaquetServeur.CONNEXION_RATE.value:    return struct.calcsize(formats_serveur_par_type[TypePaquetServeur.CONNEXION_RATE.value]) -1
            case TypePaquetServeur.MAJ_OBSTACLE.value:      return struct.calcsize(formats_serveur_par_type[TypePaquetServeur.MAJ_OBSTACLE.value]) -1
    except Exception as e:
        print(f"DANS LONGUEUR {e}")
        exit()


def deconstruire_superpaquet(superpaquet: list[tuple[TypePaquetServeur, bytes]]) -> dict[str, any]:
    pass

