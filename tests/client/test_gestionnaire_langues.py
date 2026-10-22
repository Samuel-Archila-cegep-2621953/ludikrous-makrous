# import pytest
from .. import 

def test_obtenir():
    resultat_attendu = "Fermer"
    k = "menu_principal.bouton.fermer"
    lang = "fr"

    resultat = GestionnaireLangues.obtenir(k, lang)

    assert resultat == resultat_attendu