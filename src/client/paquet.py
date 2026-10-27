import struct
from type_paquet import TypePaquetClient, TypePaquetServeur

def lire_paquet(paquet: bytes):
    _type = struct.unpack('B', paquet[:1])[0]
    match _type:
        case TypePaquetServeur.MAJ_JOUEUR.value:
            _paquet = struct.unpack('BIfff16sBB', paquet)