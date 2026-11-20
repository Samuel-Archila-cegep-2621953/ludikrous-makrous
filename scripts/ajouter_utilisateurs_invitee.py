import sqlite3
import hashlib
from pathlib import Path

_mdp = hashlib.sha256(hashlib.sha256(b'\x00').digest()).hexdigest()
print(_mdp)

_bd = sqlite3.connect(Path(__file__).parent.parent / "src" / "serveur" / "serveur.db", check_same_thread = False)
_curseur = _bd.cursor()
    
_curseur.execute("""
CREATE TABLE IF NOT EXISTS utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pseudonyme TEXT UNIQUE NOT NULL,
    mot_de_passe TEXT NOT NULL,
    date_creation TEXT DEFAULT (datetime('now', 'localtime'))
)
""")
_bd.commit()

for i in range(2048):
    _nom = f'u{i}'

    _curseur.execute("INSERT INTO utilisateurs (pseudonyme, mot_de_passe) VALUES (?, ?)", (_nom, _mdp))
    _bd.commit()