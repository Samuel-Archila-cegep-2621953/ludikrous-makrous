from enum import Enum

class TypeJeu(Enum):
    SEUL = 0      # En pratique, même chose que TypeJeu.HEBERGER, mais avec IP = localhost
    HEBERGER = 1  
    EN_LIGNE = 2