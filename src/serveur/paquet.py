import struct
import joueur_abstrait
import monde_serveur
from type_paquet import TypePaquetServeur, TypePaquetClient, formats_serveur_par_type
import hashlib

def creer_paquet_joueur(joueur: joueur_abstrait.JoueurAbstrait) -> bytes:
    """
    Formatte un joueur abstrait en paquet binaire. \n
    Format: `BIfff16sBB`
    - type         (`uint8_t`)
    - ID           (`uint32_t`)
    - nom          (`char[16]`)
    - position X   (`float`)
    - position Y   (`float`)
    - position Z   (`float`)
    - vie          (`uint8_t`)
    - animation    (`uint8_t`)
    Args:
        joueur (JoueurAbstrait): joueur
    Returns:
        bytes: paquet
    """
    #TODO!: Je pense que "s" devrait être remplacé par "<longueur_nom_utlisateur_max>s" pour qu'il soit interprété comme n * nb_chars. Il faudrait aussi soit: 1) Limiter les caractères permis a ascii ou 2) Compter le nombres de bytes (non de caractères) saisis de l'utlisateur avant de confirmer le nom d'utilisateur
    # 2026-10-26: J'ai changé pour rajouter un maximum de 16 caractères
    return struct.pack(formats_serveur_par_type[TypePaquetServeur.MAJ_JOUEUR.value], 
                       TypePaquetServeur.MAJ_JOUEUR.value, 
                       joueur.id,
                       joueur.nom.encode(),
                       joueur.position[0], joueur.position[1], joueur.position[2],
                       joueur.vie,
                       joueur.animation)

def creer_paquet_connexion_reussit(code: bytes) -> bytes:
    """
    Formatte la réponse lorsqu'une connexion est réussit
    Format: `B32s`
    """
    return struct.pack(formats_serveur_par_type[TypePaquetServeur.CONNEXION_REUSSIT.value],
                       TypePaquetServeur.CONNEXION_REUSSIT.value,
                       code)

def creer_paquet_connexion_rate() -> bytes:
    """
    Formatte la réponse lorsqu'une connexion est raté
    Format: `B`
    """
    return struct.pack(formats_serveur_par_type[TypePaquetServeur.CONNEXION_RATE.value], TypePaquetServeur.CONNEXION_RATE.value)


def construire_paquet(paquets: list[bytes]) -> bytes:
    """
    Formatte la réponse du serveur avec plusieurs paquets
    Format: `H(B...)`
    - Nombre de paquets (`uint16_t`)
    
    À répétition:
        - Type du paquet (`uint8_t`)
        - ... (`...`)
    """
    _format = 'H'
    _taille = struct.pack(_format, len(paquets))
    _paquet = _taille
    for _ in paquets:
        _paquet += _
    return _paquet


def lire_paquet(paquet: bytes):
    _type = struct.unpack('B', paquet[:1])[0]
    match _type:
        case TypePaquetClient.MAJ_JOUEUR.value:
            _paquet = struct.unpack('BIfff16sBB', paquet)
        case TypePaquetClient.CONNEXION.value:
            _paquet = struct.unpack('B16s32s', paquet)
        case TypePaquetClient.CREATION_COMPTE.value:
            _paquet = struct.unpack('B16s32s', paquet)
        
    
        


_joueur = joueur_abstrait.JoueurAbstrait()
_joueur.position = (10, 20, 30)
_joueur.animation = 0
_joueur.vie = 100
_joueur.id = 0
_joueur.nom = "Test"
lire_paquet(creer_paquet_joueur(_joueur))

print(len(hashlib.sha256(b"Test").digest()))