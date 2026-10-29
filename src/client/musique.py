from utilitaires import aleatoire_dans_dir
from types_musique import TypesMusique
from ursina import *
import time


class Musique(Audio):
    def __init__(
            self,
            type_musique: TypesMusique,
            aleatoire: bool = True,
            repeter_aleatoire: bool = True,
            sound_file_name: str = '', 
            volume: int = 0.5,
            boucle: bool = False,
            autoplay: bool = True,
            **kwargs: any
        ):

        if sound_file_name == '':
            sound_file_name = Musique.aleatoire(type_musique)

        if repeter_aleatoire:
           boucle = False

        #print(f"ID AVANT: {id(self)}")

        super().__init__(sound_file_name, volume, loop=boucle, autoplay=autoplay, **kwargs)
        #print(f"ID APRES: {id(self)}")

        self.__type_musique: TypesMusique = type_musique
        self.__repeter_aleatoire = repeter_aleatoire
        #self.__chemin_fichier_musique = sound_file_name
        #self.__vol = volume
        #self.__repeter = loop
        #self.__lecture_automatique = autoplay
        #print(str(self.temps) + " - - - - - INIT")
        #print(str(self.temps) + " - - - - - INIT")
        #print("Musique creee:", id(self), "Clip:", id(self.clip))
        #print(self.__chemin_fichier_musique)
        #print(id(self))


    def remplacer_par_aleatoire(self):
        """
        Remplace l'objet musique actuel par un nouvel objet musique aléatoire du même type.
        """
        self.clip = Musique.aleatoire(self.__type_musique)
        self.play()

    
    def update(self):
        if not self.playing:
            if self.__repeter_aleatoire: # Quand la musique arrête et que __repeter_aleatoire est vrai, appeler remplacer_par_aleatoire()
                self.remplacer_par_aleatoire()
            #print("changement de musique aléatoire")

    @staticmethod
    def aleatoire(t: TypesMusique):
        CHEMIN_MUSIQUE = "ressources/sons/musique/"
        chemin = t.comme_chemin()

        try:
            choix: str = aleatoire_dans_dir(CHEMIN_MUSIQUE + chemin)
        except:
            return "ressources/sons/erreur.mp3"

        return CHEMIN_MUSIQUE + chemin + choix


    def arreter(self):
        if self.playing == False: return
        self.stop(False)

    #def stop(self, destroy: bool = False):
     #   super().stop(destroy = False)



