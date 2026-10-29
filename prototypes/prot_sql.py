import sqlite3

# Créer (ou ouvrir) le fichier de bdd

db = sqlite3.connect("ma_db.db")

# Créer un curseur pour executer les requetes
cursor = db.cursor()

# Créer une requete pour générer une table (USERS)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    date_creation TEXT DEFAULT (datetime('now', 'localtime'))
)
""")

# Inserer une ligne (un utilisateur) dans la base
cursor.execute("INSERT INTO users (nom, prenom, email) VALUES (?, ?, ?)", ('Capron', 'Lea', 'lea.capron@gmail.com'))

# Executer les requetes
db.commit()