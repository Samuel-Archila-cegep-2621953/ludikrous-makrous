class Pilier:
    DUREE = 7
    def hauteur_depuis_mode(mode: int) -> float:
        # mode range 1..=5
        #return mode - 3
        match mode:
            case 0: return -15
            case 1: return -3
            case 2: return 4.5
            case 3: return 2
            case 4: return -1
            case 5: return 4