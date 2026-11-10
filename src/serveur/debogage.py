import journal

class Debogage:
    NIVEAU_VERBOSITE: int = 5

    @staticmethod
    def err(msg: str, niveau: int = 1):
        """
        Montre les erreurs selon le niveau de verbosité actuel
        Args:
            msg (str): Le message d'erreur
            niveau (int): Le niveau de danger associé à cette erreur
        """
        if Debogage.NIVEAU_VERBOSITE >= niveau:
                journal.inserer_erreur(msg + '\n')


    @staticmethod
    def avis(msg: str, niveau: int = 1):
        """
        Montre les avertissements selon le niveau de verbosité actuel
        Args:
            msg (str): Le message d'avertissement
            niveau (int): Le niveau de danger associé à cet avertissement
        """
        if Debogage.NIVEAU_VERBOSITE >= niveau:
                journal.inserer_avertissement(msg +'\n')


    @staticmethod
    def info(msg: str, niveau: int = 1):
        """
        Montre un message selon le niveau de verbosité actuel
        Args:
            msg (str): Le message
            niveau (int): Le niveau de verbosité associé au message
        """
        if Debogage.NIVEAU_VERBOSITE >= niveau:
                journal.inserer_info(msg + '\n')


    @staticmethod
    def verbosite(niveau: int):
        if niveau < 0: raise ValueError("Un niveau de verbosité ne peut pas être négatif.")
        if not isinstance(niveau, int): raise TypeError("Un niveau de verbosité doit être un int positif >= 0.")
        Debogage.NIVEAU_VERBOSITE = niveau