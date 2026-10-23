from enum import Enum

class TypesMusique(Enum):
    MENU_PRINCIPAL = 0 # tuff
    JEU_FACILE = 1
    JEU_MOYEN = 2
    JEU_DIFFICILE = 3
    PERTE = 4
    VICTOIRE = 5
    FIN = 7

    def comme_chemin(self) -> str:
        """
        Return:
            Le dossier correspondant à la musique demandée
        """
        _dir = ""
        match self:
            case self.MENU_PRINCIPAL: _dir = "menu_principal/"
            case self.JEU_FACILE:     _dir = "jeu/facile/"
            case self.JEU_MOYEN:      _dir = "jeu/moyen/"
            case self.JEU_DIFFICILE:  _dir = "jeu/difficile/"
            case self.PERTE:          _dir = "jeu/perte/"
            case self.VICTOIRE:       _dir = "jeu/victoire/"
            case self.FIN:            _dir = "jeu/fin/"

        return _dir
