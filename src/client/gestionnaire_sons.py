from abc import ABC,  abstractmethod

class GestionnaireSons(ABC):
    @abstractmethod
    def aleatoire(chemin: str) -> str:
        """
        Args:
            chemin (str): Le type/catégorie de sons
        Returns:
            Le chemin vers le fichier choisi aléatoirement
        """

