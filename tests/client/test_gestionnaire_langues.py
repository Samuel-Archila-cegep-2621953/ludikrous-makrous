import pytest
from gestionnaire_langues import GestionnaireLangues

def test_obtenir():
    resultat_attendu = "Fermer"
    k = "menu_principal.bouton.fermer"
    lang = "fr"

    resultat = GestionnaireLangues.obtenir(k, lang)

    #print("hello")
    assert resultat == resultat_attendu