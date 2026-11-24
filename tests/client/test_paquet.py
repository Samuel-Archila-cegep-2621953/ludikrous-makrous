from paquet import interpreter_paquet, lire_paquet, longueur_paquet, deconstruire_superpaquet
from type_paquet import *
from type_obstacle import *
import pytest

def test_lire_paquet():
    paquet_bytes: bytes = bytes.fromhex("05 00 01")
    tuple_attendu = (TypePaquetServeur.MAJ_OBSTACLE, (5, 0, 1))
    
    assert lire_paquet((TypePaquetServeur.MAJ_OBSTACLE, paquet_bytes)) == tuple_attendu
    
def test_interpreter_paquet():
    tuple_paquet = (TypePaquetServeur.MAJ_OBSTACLE, (5, 0, 1))
    dict_attendu = {
        "Obstacle": {
            "Type": 5,
            "Coord": (0,1)
        }
    }
    
    assert interpreter_paquet(tuple_paquet) == dict_attendu
    
@pytest.mark.parametrize("type_paquet, longueur", [
    (TypePaquetServeur.MAJ_JOUEUR.value, 4 + 16 + 3 * 4 + 1 + 1 + 4),
    (TypePaquetServeur.CONNEXION_REUSSIT.value, 4 + 32),
    (TypePaquetServeur.CONNEXION_RATE.value, 0),
    (TypePaquetServeur.MAJ_OBSTACLE.value, 0),
    (TypePaquetServeur.DECONNEXION.value, 0),
])
def test_longueur_paquet(type_paquet, longueur):
    assert longueur_paquet(type_paquet) == longueur
    
def test_deconstruire_superpaquet():
    superpaquet = [
        (TypePaquetServeur.MAJ_OBSTACLE, bytes.fromhex("05 00 01")),
        (TypePaquetServeur.MAJ_OBSTACLE, bytes.fromhex("05 10 0A")),
    ]
    
    attendu = {
        "Joueurs": [],
        "Obstacles": [
            {
                "Type": 5,
                "Coord": (0, 1)
            },
            {
                "Type": 5,
                "Coord": (16, 10)
            }
        ],
        "Connexion": {},
        "Joueurs quittés": [],
        "Session": b''
    }
    
    assert deconstruire_superpaquet(superpaquet) == attendu