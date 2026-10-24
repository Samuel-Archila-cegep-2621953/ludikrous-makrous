from gestionnaire_sons import GestionnaireSons
from utilitaires import aleatoire_dans_dir
from types_musique import TypesMusique
from ursina import *


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

        self.__audio = super().__init__(sound_file_name, volume, loop=boucle, autoplay=autoplay, **kwargs)

        self.__type_musique: TypesMusique = type_musique
        self.__repeter_aleatoire = repeter_aleatoire
        self.__sound_file_name = sound_file_name
        self.__vol = volume
        #self.__loop = loop
        self.__autoplay = autoplay
        #TODO!: FRANCAIS



    def remplacer_par_aleatoire(self):
        """
        Remplace l'objet musique actuel par un nouvel objet musique aléatoire du même type.
        """
        self.clip = Musique.aleatoire(self.__type_musique)
        self.play()

    
    #TODO!: Reverifier
    def remplacer_par_nouveau_type(self, nouveau_type: TypesMusique):
        """
        Remplace l'objet musique actuel par un nouvel objet musique aléatoire d'un nouveau type.
        """
        nouvelle_musique = Musique(nouveau_type, aleatoire=True, repeter_aleatoire=True)
        self.remplacer(nouvelle_musique)


    def update(self):
        if not self.playing:
            if self.__repeter_aleatoire:
                self.remplacer_par_aleatoire()
                print("changement de musique aléatoire")
            else:
                self.on_destroy = Musique.remplacer_par_aleatoire

    @staticmethod
    def aleatoire(t: TypesMusique):
        CHEMIN_MUSIQUE = "ressources/sons/musique/"
        chemin = t.comme_chemin()

        try:
            choix: str = aleatoire_dans_dir(CHEMIN_MUSIQUE + chemin)
        except:
            return "ressources/sons/erreur.mp3"

        return CHEMIN_MUSIQUE + chemin + choix



