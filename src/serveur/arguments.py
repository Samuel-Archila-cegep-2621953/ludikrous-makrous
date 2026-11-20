import variable_globale
import sys

def gerer_arguments():
    if '-g' in sys.argv or '--gui' in sys.argv or '--graphique' in sys.argv:
        variable_globale.interface_graphique = True
    if '-p' in sys.argv or '--port' in sys.argv:
        try:
            ind = next(i+1 for i, val in enumerate(sys.argv) if val == '-p' or val == '--port')
            variable_globale.port = ind
        except:
            print("Erreur dans l'argument -p ou --port")
            exit(0)
    if '-i' in sys.argv or '--ip' in sys.argv:
        try:
            ind = next(i+1 for i, val in enumerate(sys.argv) if val == '-i' or val == '--ip')
            variable_globale.ip = ind
        except:
            print("Erreur dans l'argument -i ou --ip")
            exit(0)