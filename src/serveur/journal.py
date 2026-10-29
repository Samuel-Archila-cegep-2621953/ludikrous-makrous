

__journal = []
__nouveau = []

def inserer_info(texte: str):
    print(f"[INFO] {texte}")
    __journal.append(('info', texte))
    __nouveau.append(('info', texte))

def inserer_erreur(texte: str):
    print(f"[ERR] {texte}")
    __journal.append(('erreur', texte))
    __nouveau.append(('erreur', texte))

def inserer_commande(commande: list[str]):
    commande_string = ' '.join(commande)
    __journal.append(('commande', commande_string))
    __nouveau.append(('commande', commande_string))
def inserer_reponse(texte: str):
    print(texte)
    __journal.append(('reponse', texte))
    __nouveau.append(('reponse', texte))

def obtenir_journal() -> list[tuple[str,str]]:
    return __journal.copy()

def obtenir_texte() -> str:
    resultat = ''
    for i in __nouveau:
        if i[0] == 'info':
            resultat += f"[INFO] {i[1]}\n"
        elif i[0] == 'erreur':
            resultat += f"[ERR] {i[1]}\n"
        elif i[0] == 'commande':
            resultat += f"> {i[1]}\n"
        elif i[0] == 'reponse':
            resultat += f"{i[1]}\n"
    __nouveau.clear()
    return resultat