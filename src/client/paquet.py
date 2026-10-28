import struct
from type_paquet import *


def lire_paquet(paquet: bytes) -> tuple[any]:
    """
    Lit un paquet et l'exporte en tuple.
    """
    try:
        _type = struct.unpack('B', paquet[:1])[0]
        if _type < TypePaquetClient.MAX.value:
            return struct.unpack(formats_serveur_par_type[_type], paquet)
    except:
        print(f"Erreur: le format du paquet n'est pas compatible, paquet: '{paquet}'")

def interpreter_paquet(paquet: tuple, type: TypePaquetServeur) -> dict:
    match type:
        case TypePaquetServeur.MAJ_JOUEUR:
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
