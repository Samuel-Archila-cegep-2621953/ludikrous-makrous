import tuile

class Monde:
    def __init__(self, longueur: int, hauteur: int):
        self.__monde: list[list[tuile.Tuile]] = []
        for y in range(hauteur):
            _colonne_tuile = []
            for x in range(longueur):
                _tuile = tuile.Tuile(x, y)
                _colonne_tuile.append(_tuile)
            self.__monde.append(_colonne_tuile)
