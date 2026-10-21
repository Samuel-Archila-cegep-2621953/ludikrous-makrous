class JoueurAbstrait:
    def __init__(self):
        self.id = self.obtenir_id
        self.nom = self.obtenir_nom
        self.score = 0
        self.position = (0,0,0)
        self.vie = True

    def obtenir_id(self):
        """
        Demande au serveur un id unique
        """
        return self.id

    def obtenir_nom(self):
        """
        Cherche le nom déjà demandé à l'utilisateur et sauvegardé dans la configuration de l'utilisateur
        """
        return self.nom



def formatter_json(liste_joueurs: list[JoueurAbstrait]) -> list[dict]:
    # TODO Reparer ce warning    ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
    """
    Formatte une liste de JoueurAbstrait en dict pour json
    """
    json_joueurs: list[dict] = []

    for j in liste_joueurs:
        json_joueurs.append({
            "position":  j.position,
            "nom":       j.nom,
            "vie":       j.vie,
            "animation": j.animation
        })

    return json_joueurs
    # TODO Tester
