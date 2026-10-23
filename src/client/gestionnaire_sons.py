from enum import Enum
from types_musique import TypesMusique

class GestionnaireSons(Enum):
    @staticmethod
    def aleatoire(cat: TypesMusique) -> str:
        """
        Args:
            cat (TypesMusique): Le type/catégorie de musique
        Returns:
            str: Le chemin vers le fichier choisi aléatoirement
        """