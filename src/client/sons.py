from ursina import Audio
from utilitaires import aleatoire_dans_dir

class Son(Audio):
    """Représente un son qui ne se répète pas, aléatoire dans la catégorie indiquée."""

    def __init__(
            self, 
            c: str, 
            volume: float = 0.5, 
            pitch: float = 1, 
            balance: float = 0, 
            **kwargs: any
        ):
        """
        Args:
            c (str): Le son à utiliser 
        Returns:
            Son: Un son aléatoire dans la catégorie indiquée par `c`. Ne joue qu'une fois.
        """
        _chemin_son = Son.aleatoire(c)
        self.__audio = super().__init__(_chemin_son, volume, pitch, balance)


    @staticmethod
    def aleatoire(chemin: str) -> str:
        CHEMIN_SONS = "ressources/sons/sons/"
        chemin.replace('.', '/')

        try:
            choix: str = aleatoire_dans_dir(CHEMIN_SONS + chemin)
        except:
            return "ressources/sons/erreur.mp3"
        
        return CHEMIN_SONS + chemin + choix



            
