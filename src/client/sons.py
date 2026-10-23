from gestionnaire_sons import GestionnaireSons
from utilitaires import aleatoire_dans_dir

class Sons(GestionnaireSons):
    @staticmethod
    def aleatoire(chemin: str) -> str:
        CHEMIN_SONS = "ressources/sons/sons/"
        chemin.replace('.', '/')

        try:
            choix: str = aleatoire_dans_dir(CHEMIN_SONS + chemin)
        except:
            return "ressources/sons/erreur.mp4"
        
        return CHEMIN_SONS + chemin + choix



            
