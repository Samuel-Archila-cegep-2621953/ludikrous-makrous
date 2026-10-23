from gestionnaire_sons import GestionnaireSons
from utilitaires import aleatoire_dans_dir
from types_musique import TypesMusique


class Musique(GestionnaireSons):
    @staticmethod
    def aleatoire(t: TypesMusique):
        CHEMIN_MUSIQUE = "ressources/sons/musique/";
        chemin = t.comme_chemin();

        try:
            choix: str = aleatoire_dans_dir(chemin);
        except:
            return "ressources/sons/erreur.mp4";
            # TODO: Créer ressources/sons/erreur.mp4
        
        return CHEMIN_MUSIQUE + chemin + choix;



