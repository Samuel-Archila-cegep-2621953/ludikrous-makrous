import time

class JoueurAbstrait:
    def __init__(self):
        self.id = 0
        self.nom = ''
        self.score = 0
        self.position = (0,0,0)
        self.vie = 100
        self.en_vie = True
        #NOTE CHANGé vers un int pour tester. 2-11-2026. Samuel. self.animation = "pause"
        self.animation = 0
        self.dernier_paquet = time.time()


def formatter_json(liste_joueurs: list[JoueurAbstrait]) -> list[dict]:
    """
    Formatte une liste de JoueurAbstrait en dict pour json
    """
    json_joueurs: list[dict] = []

    for j in liste_joueurs:
        json_joueurs.append({
            "Position":  [j.position[0], j.position[1], j.position[2]],
            "Nom":       j.nom,
            "Vie":       j.vie,
            "En_vie": j.en_vie,
            "Animation": j.animation,
            "ID": j.id,
        })

    return json_joueurs
    # TODO Tester
