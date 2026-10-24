from gestionnaire_sons import GestionnaireSons
from utilitaires import aleatoire_dans_dir
from types_musique import TypesMusique
from ursina import *


class Musique(GestionnaireSons, Audio):
    def __init__(
            self,
            type_musique: TypesMusique,
            aleatoire: bool = True,
            prochain_aleatoire: bool = True,
            sound_file_name: str = '', 
            volume: int = 0.5,
            pitch: int = 1,
            balance: int = 0,
            loop: bool = True,
            loops: int = 1,
            autoplay: bool = True,
            auto_destroy: bool = False,
            group: str = 'sfx',
            **kwargs: any
        ):

        sound_file_name = Musique.aleatoire(type_musique) if aleatoire else sound_file_name

        self.musique: Audio = super().__init__(sound_file_name, volume, pitch, balance, loop, loops, autoplay, auto_destroy, group, **kwargs)
        self.__prochain_aleatoire: bool = prochain_aleatoire
        self.__type_musique: TypesMusique = type_musique
        self.__chemin_musique: str = sound_file_name

    def remplacer(self, musique: 'Musique'):
        """
        Remplace l'objet musique actuel par un nouvel objet musique.
        """
        # Remplacer l'objet musique actuel par le nouvel objet musique
        self.__dict__.clear()
        self.__dict__.update(musique.__dict__)

    def remplacer_par_aleatoire(self):
        """
        Remplace l'objet musique actuel par un nouvel objet musique aléatoire du même type.
        """
        if self.__prochain_aleatoire:
            nouvelle_musique = Musique(self.__type_musique, aleatoire=True, prochain_aleatoire=True)
            self.remplacer(nouvelle_musique)

    def remplacer_par_nouveau_type(self, nouveau_type: TypesMusique):
        """
        Remplace l'objet musique actuel par un nouvel objet musique aléatoire d'un nouveau type.
        """
        nouvelle_musique = Musique(nouveau_type, aleatoire=True, prochain_aleatoire=True)
        self.remplacer(nouvelle_musique)



    @staticmethod
    def aleatoire(t: TypesMusique):
        CHEMIN_MUSIQUE = "ressources/sons/musique/"
        chemin = t.comme_chemin()

        try:
            choix: str = aleatoire_dans_dir(CHEMIN_MUSIQUE + chemin)
        except Exception as e:
            return "ressources/sons/erreur.mp3"

        return CHEMIN_MUSIQUE + chemin + choix



