import struct
import joueur_abstrait
import monde_serveur
from type_paquet import TypePaquetServeur, TypePaquetClient, formats_serveur_par_type, formats_clients_par_type
import hashlib
from debogage import Debogage as Dbg

def creer_paquet_joueur(joueur: joueur_abstrait.JoueurAbstrait) -> bytes:
    #NOTE Format: `BIfff16sBB` changé. 2-11-2026
    """
    Formatte un joueur abstrait en paquet binaire. \n
    Format: `BI16sfffBB`
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
    return struct.pack(
        formats_serveur_par_type[TypePaquetServeur.MAJ_JOUEUR.value], # FORMAT
            TypePaquetServeur.MAJ_JOUEUR.value, # TYPE
            #joueur.id,
            1,
            joueur.nom.encode("ascii"),
            joueur.position[0], joueur.position[1], joueur.position[2],
            joueur.vie,
            joueur.animation
        )

def creer_paquet_deconnexion() -> bytes:
    """
    Formatte la réponse lorsque le serveur veut refuser les paquets. \n
    Format: `B`
    - type (`uint8_t`)
    Returns:
        bytes: paquet
    """
    Dbg.info("Création d'un paquet de déconnexion", 2)
    return struct.pack(formats_serveur_par_type[TypePaquetServeur.DECONNEXION.value], TypePaquetServeur.DECONNEXION.value)

def creer_paquet_connexion_reussit(code: bytes) -> bytes:
    """
    Formatte la réponse lorsqu'une connexion est réussit
    Format: `B32s`
    """
    Dbg.info("Création d'un paquet de connexion réussie", 2)
    return struct.pack(formats_serveur_par_type[TypePaquetServeur.CONNEXION_REUSSIT.value],
                       TypePaquetServeur.CONNEXION_REUSSIT.value,
                       code)

def creer_paquet_connexion_rate() -> bytes:
    """
    Formatte la réponse lorsqu'une connexion est ratée
    Format: `B`
    """
    Dbg.info("Création d'un paquet de connexion ratée", 2)
    return struct.pack(formats_serveur_par_type[TypePaquetServeur.CONNEXION_RATE.value], TypePaquetServeur.CONNEXION_RATE.value)


def construire_paquet(paquets: list[bytes]) -> bytes:
    """
    Formatte la réponse du serveur avec plusieurs paquets
    Format: `H(B...)`
    - Nombre de paquets (`uint16_t`)
    
    À répétition:
        - Type du paquet (`uint8_t`)
        - ... (`...`)
    
    Args:
        paquets (list[bytes]): paquets
    Returns:
        bytes: le paquet final
    """
    _format = '!H'
    _taille = struct.pack(_format, len(paquets))
    _paquet = _taille
    for _ in paquets:
        _paquet += _
    return _paquet


def lire_paquet(paquet: bytes) -> tuple[any]:
    """
    Lit un paquet et l'exporte en tuple.
    """
    try:
        _type = struct.unpack('!B', paquet[:1])[0]
        if _type < TypePaquetClient.MAX.value:
            return struct.unpack(formats_clients_par_type[_type], paquet)
    except:
        print(f"Erreur: le format du paquet n'est pas compatible, paquet: '{paquet}'")