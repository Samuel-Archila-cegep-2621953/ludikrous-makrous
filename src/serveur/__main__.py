import serveur
import arguments

if __name__ == '__main__':
    arguments.gerer_arguments()
    _serveur = serveur.Serveur()
    _serveur.boucle_principale()