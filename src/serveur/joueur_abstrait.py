class JoueurAbstrait:
    def __init__(self):
        self.id = 0
        self.nom = ''
        self.score = 0
        self.position = (0,0,0)
        self.vie = True


def formatter_json(liste_joueurs: list[JoueurAbstrait]) -> list[dict]:
    # TODO Reparer ce warning    ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
    """
    Formatte une liste de JoueurAbstrait en dict pour json
    """
    json_joueurs: list[dict] = []

    for j in liste_joueurs:
        json_joueurs.append({
            "Position":  [j.position[0], j.position[1], j.position[2]],
            "Nom":       j.nom,
            "Vie":       j.vie #,
            #"Animation": j.animation
        })

    return json_joueurs
    # TODO Tester
