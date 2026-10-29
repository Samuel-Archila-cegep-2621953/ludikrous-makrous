class JoueurAbstrait {
    unsigned int id, score;
    String nom;
    (int, int, int) position;
    unsigned float vie;

    fn new() -> Self {
        return JoueurAbstrait {
            id: obtenir_id(),
            score: 0,
            nom: demander_nom(),
            vie: demander_vie()
        };
    }

    fn demander_nom() -> String {
        return OBTENIR NOM_JOUEUR DU Serveur;
    }
    
    fn demander_vie() -> String {
        return OBTENIR VIE_JOUEUR DU Serveur;
    }

    fn obtenir_id() -> String {
        return Serveur::generer_id_unique();
    }
}

fn formatter_json(liste_joueurs: Vec<JoueurAbstrait>) -> Vec<HashMap> {
    json_joueurs: Vec<HashMap> = Vec::new();

    for j in liste_joueurs {
        json_joueurs.push(
            dict = HashMap::new();
            dict.add("Position", j.position);
            dict.add("Nom", j.nom);
            dict.add("Vie", j.vie);
            dict.add("Animation", j.animation);
        );
    }
}