class Joueur:
    def __init__(self):
        self.id = self.obtenir_id
        self.nom = self.obtenir_nom
        self.score = 0
        self.position = (0,0)
        self.vie = 100
        self.en_vie = True
        pass

    def mise_a_jour(self, temps_entre_update):

        if self.vie > 0:
            self.en_vie = True
        else:
            self.en_vie = False


        if self.en_vie == True:

            self.vie += 10 * temps_entre_update # regénération passive des vies



    def obtenir_id(self):
        """
        Demande au serveur un id unique
        """
        pass

    def obtenir_nom(self):
        """
        Cherche le nom déjà demandé à l'utilisateur et sauvegardé dans la configuration de l'utilisateur
        """
        pass