import struct
from type_paquet import *


def lire_paquet(tuple_paquet: tuple[TypePaquetServeur, bytes]) -> tuple[TypePaquetServeur, tuple[any]]:
    """
    Lit un paquet et l'exporte en tuple.
    """
    print(f"LEN PAQUET {len(paquet)}")
    try:
        _type = tuple_paquet[0]
        _paquet = tuple_paquet[1]
        print(f"DANS LIRE_PAQUET TYPE EST {_type}")
        #NOTE Vieux if _type < TypePaquetClient.MAX.value:
        if _type < TypePaquetServeur.MAX.value:

            return (
                _type,
                struct.unpack(
                    formats_serveur_par_type[_type.value][:1], # Enleve le char de format
                    _paquet
                )
            )

    except Exception as e:
        print(f"Erreur: le format du paquet n'est pas compatible, paquet: '{paquet}'")
        print(e)
        exit()




#NOTE VIEUX def interpreter_paquet(paquet: tuple, type: TypePaquetServeur) -> dict:
def interpreter_paquet(paquet: tuple[TypePaquetServeur, tuple[any]]) -> dict:
    if paquet is None: print("PAQUET EST NONe")
    _type = paquet[0]
    _paquet = paquet[1]
    match _type:
        case TypePaquetServeur.MAJ_JOUEUR:
            print(f"Paquet MAJ JOUEUR: {paquet}")
            x, y, z, nom, vie, animation = _paquet
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
                "Connexion": _paquet[0]
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
            case TypePaquetServeur.MAX.value:               return struct.calcsize(formats_serveur_par_type[TypePaquetServeur.MAX.value]) -1
    except Exception as e:
        print(f"DANS LONGUEUR {e}")
        exit()


