import struct
import joueur_abstrait
from type_paquet import TypePaquet

def creer_paquet_joueur(joueur: joueur_abstrait.JoueurAbstrait) -> bytes:
    """
    formatte un joueur abstrait en paquet binaire.
    Format: BIfffsBB
    - type
    - ID
    - position X
    - position Y
    - position Z
    - nom
    - vie
    - animation
    Args:
        joueur (JoueurAbstrait): joueur
    Returns:
        bytes: paquet
    """
    _format = 'BIfffsBB'
    return struct.pack(_format, 
                       TypePaquet.MAJ_JOUEUR, 
                       joueur.id, 
                       joueur.position.x, joueur.position.y, joueur.position.z,
                       joueur.nom.encode(),
                       joueur.vie,
                       joueur.animation)