from ursina import *

markous = load_model('ressources/modeles/markous.glb')

class Joueur(Entity):
    def __init__(self, id, nom, position: tuple[float,float,float], **kwargs):
        super().__init__(model=copy(markous), scale=(1,1,1), rotation=(-90, 0, 0))
        self.__ID = id
        self.__nom = nom
        self.__score = 0
        self.position = position
        self.__vie = 100
        self.__en_vie = True

    def nom(self) -> str:
        return self.__nom

    def changer_nom(self, nouveau_nom):
        self.__nom = nouveau_nom

    def mise_a_jour(self, temps_entre_update):

        if self.vie > 0:
            self.en_vie = True
        else:
            self.en_vie = False


        if self.en_vie == True:

            self.vie += 10 * temps_entre_update # regénération passive des vies