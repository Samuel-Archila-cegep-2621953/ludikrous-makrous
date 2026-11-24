import pytest
from gestionnaire_langues import GestionnaireLangues

@pytest.mark.parametrize("k, lang, resultat", [
    ("menu_principal.boutons.fermer", "es", "Cerrar"),
    ("menu_config.boutons.langues", "fr", "Langues"),
    ("jeu.texte.spectateur", "en", "Spectator"),
    ("jeu.texte.spectateur", "es", "Espectador"),
    ("menu_config.texte.nom_affichage", "es", "Nombre público"),
    ("menu_config.texte.mot_de_passe", "es", "Contraseña"),
    ("menu_principal.boutons.jouer_seul", "en", "Singleplayer"),
    ("menu_principal.boutons.config", "fr", "Paramètres"),
])
def test_obtenir(k: str, lang: str, resultat: str):
    resultat_obtenu = GestionnaireLangues.obtenir(k, lang)

    #print("hello")
    assert resultat == resultat_obtenu
