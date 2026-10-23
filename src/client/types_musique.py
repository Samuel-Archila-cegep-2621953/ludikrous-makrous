from enum import Enum

class TypesMusique(Enum):
    MENU_PRINCIPAL = 0 # tuff
    JEU_FACILE = 1
    JEU_MOYEN = 2
    JEU_DIFFICILE = 3
    PERTE = 4
    VICTOIRE = 5
    FIN = 7

    def comme_chemin(self):
        match self:
            case self.MENU_PRINCIPAL: "menu_principal"