from enum import Enum

class GestionnaireMusique(Enum):
    MENU_PRINCIPAL = 0
    JEU_FACILE = 1
    JEU_MOYEN = 2
    JEU_DIFFICILE = 3
    PERTE = 4
    VICTOIRE = 5
    FIN = 7
    
    @staticmethod
    def aleatoire(cat: GestionnaireMusique) -> str:
        """
        Args:
            cat (GestionnaireMusique): Le type/catégorie de musique
        Returns:
            str: Le chemin vers le fichier choisi aléatoirement
        """
        pass