import customtkinter as ctk

__journal = []
__nouveau = []

def inserer_info(texte: str):
    print(f"(i) {texte}")
    __journal.append(('info', texte))
    __nouveau.append(('info', texte))

def inserer_erreur(texte: str):
    print(f"🞭 {texte}")
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
def inserer_avertissement(texte: str):
    print(f"⚠ {texte}")
    __journal.append(('avertissement', texte))
    __nouveau.append(('avertissement', texte))

def obtenir_journal() -> list[tuple[str,str]]:
    return __journal.copy()

def obtenir_texte(journal: ctk.CTkTextbox) -> str:
    _derniere_ligne: int = len(journal.get('1.0', ctk.END).splitlines())
    for idx, i in enumerate(__nouveau):
        if i[0] == 'info':
            journal.insert(ctk.END, f"(i) {i[1]}\n")
        elif i[0] == 'erreur':
            journal.insert(ctk.END, f"🞭 {i[1]}\n")
        elif i[0] == 'commande':
            journal.insert(ctk.END, f"❱ {i[1]}\n")
        elif i[0] == 'avertissement':
            journal.insert(ctk.END, f"⚠ {i[1]}\n")
        elif i[0] == 'reponse':
            journal.insert(ctk.END, f"{i[1]}\n")
        journal.tag_add(i[0], f"{_derniere_ligne+idx}.0", f"{_derniere_ligne+idx+1}.5")
        journal.yview(ctk.END)
    __nouveau.clear()