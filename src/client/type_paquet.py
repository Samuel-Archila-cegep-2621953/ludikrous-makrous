import enum

class TypePaquetServeur(enum.Enum):
    MAJ_JOUEUR = 0,
    CONNEXION_REUSSIT = 1,
    CONNEXION_RATE = 2,

class TypePaquetClient(enum.Enum):
    MAJ_JOUEUR = 0,
    CONNEXION = 1,
    CREATION_COMPTE = 2
    OBTENIR_JOUEURS = 3

formats_serveur_par_type = [
    'BIfff16sBB',
    'B32s',
    'B'
]

formats_clients_par_type = [
    "B32sfffBB", # Type, hache clé, x, y, z, vie, animation
    "B16s32s", # Type, nom, mdp haché
    "B16s32s" # Type, nom, mdp haché
]