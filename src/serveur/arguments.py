import variable_globale
import sys

def gerer_arguments():
    if '-g' in sys.argv or '--gui' in sys.argv or '--graphique' in sys.argv:
        variable_globale.interface_graphique = True
    if '-p' in sys.argv or '--port' in sys.argv:
        try:
            ind = next(i for i, val in enumerate(sys.argv) if val == '-p')
            variable_globale.port = ind + 1
        except:
            print("Erreur dans l'argument -p ou --port")
            exit(0) 