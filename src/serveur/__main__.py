import serveur
import arguments
import journal
import sys

if __name__ == '__main__':
    arguments.gerer_arguments()
    _serveur = serveur.Serveur()
    _serveur.boucle_principale()