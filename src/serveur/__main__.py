import serveur
import base_de_donnees
import hashlib

if __name__ == '__main__':
    _bd = base_de_donnees.BaseDeDonnees()

    if input("connexion? (O/n) ").lower() == 'o':
        while True:
            _utilisateur = input("Utilisateur? ")
            _mot_de_passe = hashlib.sha256(input("Mot-de-passe? ").encode()).hexdigest()
            if _bd.connexion(_utilisateur, _mot_de_passe):
                print("Connecté!")
                break
            else:
                print("Nom ou mot-de-passe incorrect.")
    else:
        while True:
            _utilisateur = input("Utilisateur? ")
            _mot_de_passe = hashlib.sha256(input("Mot-de-passe? ").encode()).hexdigest()
            if not _bd.creer_utilisateur(_utilisateur, _mot_de_passe):
                print("Utilisateur déjà existant.")
    
    _serveur = serveur.Serveur()
    _serveur.boucle_principale()