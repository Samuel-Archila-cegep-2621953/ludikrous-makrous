import enum

class TypePaquetServeur(enum.Enum):
    MAJ_JOUEUR =        0
    CONNEXION_REUSSIT = 1
    CONNEXION_RATE =    2
    #DECONNEXION =       3
    #MAJ_OBSTACLE =      4
    MAJ_OBSTACLE =      3
    DECONNEXION =       4

    @staticmethod
    def depuis_int(n: int) -> "TypePaquetServeur":
        match n:
            case 0: return TypePaquetServeur.MAJ_JOUEUR
            case 1: return TypePaquetServeur.CONNEXION_REUSSIT
            case 2: return TypePaquetServeur.CONNEXION_RATE
            #case 3: return TypePaquetServeur.DECONNEXION
            #case 4: return TypePaquetServeur.MAJ_OBSTACLE
            case 3: return TypePaquetServeur.MAJ_OBSTACLE
            case 4: return TypePaquetServeur.DECONNEXION

    @staticmethod
    def max() -> int:
        #NOTE Peut probablement être amélioré
        return 4

class TypePaquetClient(enum.Enum):
    MAJ_JOUEUR = 0
    CONNEXION = 1
    CREATION_COMPTE = 2
    DECONNEXION = 3
    MAX = 4

formats_serveur_par_type = [
    #'BIfff16sBB', NOTE Apparement changé coté serveur pour \/
    'B!I16siiiBBf',
    'B!I32s',
    'B!',

    #'B32s' NOTE ?
    'B!', # Obstacle: Ceci + format spécifique au type
    'B!'
    #TODO FORMAT OBSTACLE
]

formats_clients_par_type = [
    "!B32siiiBBf", # Type, hache clé, x * 100, y * 100, z * 100, vie, animation; TODO! Confirmer "hache clé" / ajout rotation
    "!B16s32s", # Type, nom, mdp haché
    "!B16s32s", # Type, nom, mdp haché
    "!B32s" # Type, session
]