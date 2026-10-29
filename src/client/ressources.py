from pathlib import Path

def obtenir_ressources() -> Path:
    return Path(__file__).parent / 'ressources'