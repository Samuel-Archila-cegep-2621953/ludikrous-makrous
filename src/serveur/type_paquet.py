import enum

class TypePaquetServeur(enum.Enum):
    MAJ_JOUEUR = 0
    CONNEXION_REUSSIT = 1
    CONNEXION_RATE = 2
    OBSTACLE = 3
    DECONNEXION = 4

class TypePaquetClient(enum.Enum):
    MAJ_JOUEUR = 0,
    CONNEXION = 1,
    CREATION_COMPTE = 2,
    DECONNEXION = 3,
    MAX = 4

formats_serveur_par_type = [
    '!BI16siiiBBf',
    '!BI32s',
    '!B',
    '!B', # Obstacle: Ceci + format spécifique au type
    '!B'
]

formats_clients_par_type = [
    "!B32siiiBBf", # Type, hache clé, x, y, z, vie, animation
    "!B16s32s", # Type, nom, mdp haché
    "!B16s32s", # Type, nom, mdp haché
    "!B32s" # Type, session
]