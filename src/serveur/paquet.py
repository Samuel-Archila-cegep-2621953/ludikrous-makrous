import struct
import joueur_abstrait
from type_paquet import TypePaquet

def creer_paquet_joueur(joueur: joueur_abstrait.JoueurAbstrait) -> bytes:
    """
    Formatte un joueur abstrait en paquet binaire. \n
    Format: `BIfffsBB`
    - type         (`unsigned char`)
    - ID           (`unsigned int`)
    - position X   (`float`)
    - position Y   (`float`)
    - position Z   (`float`)
    - nom          (`char[]`)
    - vie          (`unsigned char`)
    - animation    (`unsigned char`)
    Args:
        joueur (JoueurAbstrait): joueur
    Returns:
        bytes: paquet
    """
    #TODO!: Je pense que "s" devrait être remplacé par "<longueur_nom_utlisateur_max>s" pour qu'il soit interprété comme n * nb_chars. Il faudrait aussi soit: 1) Limiter les caractères permis a ascii ou 2) Compter le nombres de bytes (non de caractères) saisis de l'utlisateur avant de confirmer le nom d'utilisateur
    _format = 'BIfffsBB'
    return struct.pack(_format, 
                       TypePaquet.MAJ_JOUEUR, 
                       joueur.id,
                       joueur.position.x, joueur.position.y, joueur.position.z,
                       joueur.nom.encode(),
                       joueur.vie,
                       joueur.animation)