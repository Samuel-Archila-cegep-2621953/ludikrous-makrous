import enum

class TypePaquetServeur(enum.Enum):
    MAJ_JOUEUR = 0
    CONNEXION_REUSSIT = 1
    CONNEXION_RATE = 2
    MAJ_OBSTACLE = 3
    MAX = 4

    @staticmethod
    def depuis_int(n: int) -> "TypePaquetServeur":
        match n:
            case 0: return TypePaquetServeur.MAJ_JOUEUR
            case 1: return TypePaquetServeur.CONNEXION_REUSSIT
            case 2: return TypePaquetServeur.CONNEXION_RATE
            case 3: return TypePaquetServeur.MAJ_OBSTACLE
            case 4: return TypePaquetServeur.MAX

class TypePaquetClient(enum.Enum):
    MAJ_JOUEUR = 0
    CONNEXION = 1
    CREATION_COMPTE = 2
    MAX = 3

formats_serveur_par_type = [
    'BIfff16sBB',
    'B32s',
    'B',
    #TODO FORMAT OBSTACLE
]

formats_clients_par_type = [
    "B32sfffBB", # Type, hache clé, x, y, z, vie, animation; TODO! Confirmer "hache clé"
    "B16s32s", # Type, nom, mdp haché
    "B16s32s" # Type, nom, mdp haché
]