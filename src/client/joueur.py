from ursina import *

class Joueur(Entity):
    def __init__(self, id, nom, position: tuple[float,float,float], **kwargs):
        super().__init__(model='cube', color=rgb(0,0,0), scale=(1,2.5,1))
        self.alpha_setter(0.5)
        self.__ID = id
        self.__nom = nom
        self.__score = 0
        self.position = position
        self.__vie = 100
        self.__en_vie = True

    def nom(self) -> str:
        return self.__nom

    def nom(self, nouveau_nom):
        self.__nom = nouveau_nom

    def mise_a_jour(self, temps_entre_update):

        if self.vie > 0:
            self.en_vie = True
        else:
            self.en_vie = False


        if self.en_vie == True:

            self.vie += 10 * temps_entre_update # regénération passive des vies