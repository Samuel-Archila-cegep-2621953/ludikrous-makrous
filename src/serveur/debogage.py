import journal

class Debogage:
    NIVEAU_VERBOSITE: int = 1

    @staticmethod
    def err(msg: str, niveau: int = 1, avertissement: bool = False):
        """
        Montre les erreurs selon le niveau de verbosité actuel
        Args:
            msg (str): Le message d'erreur ou d'avertissement
            niveau (int): Le niveau de danger associé à cette erreur/avertissement
            avertissement (bool): Si le message est un avertissement ou non
        """
        if avertissement:
             journal.inserer_avertissement(msg)
             return

        if Debogage.NIVEAU_VERBOSITE == niveau:
                journal.inserer_erreur(msg)


    @staticmethod
    def verbosite(niveau: int):
        if niveau < 0: raise ValueError("Un niveau de verbosité ne peut pas être négatif.")
        if not isinstance(niveau, int): raise TypeError("Un niveau de verbosité doit être un int positif >= 0.")
        Debogage.NIVEAU_VERBOSITE = niveau