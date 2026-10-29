from collections.abc import Callable
#from constantes import TICKS_JEU_PAR_SECONDE

class ModificateurDifficulte:
    #TODO: Playtest
    @staticmethod
    def fonction_difficulte(niveau: int) -> Callable[[float], float]:
        """
        Args:
            niveau: Le niveau de difficulté
        Returns:
            Callable[[float], float]: Une fonction qui prend un float et retourne un float modifié, soit la fonction utilisée pour mettre à jour la difficulté du jeu. La fonction accepte un valeur en
        """
        match niveau:
            case 0: return lambda t: t * 0.19
            case 1: return lambda t: t * 1
            case 2: return lambda t: t ** 2 * 0.002
            case 3: return lambda t: 1.0022 **t * 1.25
            case 4: return lambda t: t * 1.5
