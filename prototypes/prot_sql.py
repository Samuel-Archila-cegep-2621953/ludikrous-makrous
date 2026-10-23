import sqlite3

# Créer (ou ouvrir) le fichier de bdd

db = sqlite3.connect("ma_db.db")

# Créer un curseur pour executer les requetes
cursor = db.cursor()

# Créer une requete pour générer une table (USERS)