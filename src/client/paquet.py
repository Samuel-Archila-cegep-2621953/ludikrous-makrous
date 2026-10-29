import struct
from type_paquet import *


def lire_paquet(paquet: bytes) -> tuple[any]:
    """
    Lit un paquet et l'exporte en tuple.
    """
    print(f"LEN PAQUET {len(paquet)}")
    try:
        _type = struct.unpack('B', paquet[:1])[0]
        print(f"DANS LIRE_PAQUET TYPE EST {_type}")
        #NOTE Vieux if _type < TypePaquetClient.MAX.value:
        if _type < TypePaquetServeur.MAX.value:
            return struct.unpack(formats_serveur_par_type[_type], paquet)
    except Exception as e:
        print(f"Erreur: le format du paquet n'est pas compatible, paquet: '{paquet}'")
        print(e)
        exit()

#NOTE VIEUX def interpreter_paquet(paquet: tuple, type: TypePaquetServeur) -> dict:
def interpreter_paquet(paquet: tuple) -> dict:
    if paquet is None: print("PAQUET EST NONe")
    _type = paquet[0]
    match _type:
        case TypePaquetServeur.MAJ_JOUEUR:
            print(f"Paquet MAJ JOUEUR: {paquet}")
            _, x, y, z, nom, vie, animation = paquet
            return {
                "Joueurs": [{
                    "ID": 123,
                    "Position": [x, y, z],
                    "Nom": nom,
                    "En_vie": vie,
                    "Animation": animation
                }]
            }

        case TypePaquetServeur.CONNEXION_RATE:
            print("\033[91mErreur de connexion")

        case TypePaquetServeur.CONNEXION_REUSSIT:
            print("\033[91mConnection réussie")

def longueur(b: bytes) -> int:
    """
    Prend 1 byte est retourne la grandeur du message qui le suit selon son type
    """
    try:
        match int.from_bytes(b):
            case TypePaquetServeur.MAJ_JOUEUR.value:        return struct.calcsize(formats_serveur_par_type[TypePaquetServeur.MAJ_JOUEUR.value])
            case TypePaquetServeur.CONNEXION_REUSSIT.value: return struct.calcsize(formats_serveur_par_type[TypePaquetServeur.CONNEXION_REUSSIT.value])
            case TypePaquetServeur.CONNEXION_RATE.value:    return struct.calcsize(formats_serveur_par_type[TypePaquetServeur.CONNEXION_RATE.value])
            case TypePaquetServeur.MAX.value:               return struct.calcsize(formats_serveur_par_type[TypePaquetServeur.MAX.value])
    except Exception as e:
        print(f"DANS LONGUEUR {e}")
        exit()