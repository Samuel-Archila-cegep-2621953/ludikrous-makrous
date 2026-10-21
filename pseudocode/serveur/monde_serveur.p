class MondeServeur:
    Vec<u8, u8> dimensions;
    float difficulte_globale, temps_de_jeu;
    Vec<JoueurAbstrait> joueurs;
    Vec<Modificateur> modificateurs;
    Vec<Messages> liste_messages;
    Vec<Obstacle> liste_obstacles;

    fn new() -> Self {}
        
        dimensions = [8,8] # grille 8 x 8
        self.__difficulte_globale = 0
        self.__dimensions: list[int] = dimensions # grandeur de la grille, par défaux 8x8
        self.__joueurs: list[JoueurAbstrait] = [] # Liste de joueurs
        self.__liste_modificateur = []
        self.__temps_de_jeu = 0.0
        self.__partie_en_cours = False

        self.__liste_message = []

        self.__liste_obstacle = []
        

    fn formatter_json(self):
        """
        Formatte le monde du serveur en json pour l'envoyer au client.
        Style:
            {
                "general": {
                    "temps_de_jeu": <__temps_de_jeu>,
                    "liste_message": <SignalServeurClient> 
                },

                "nouveaux_obstacles": [
                    {
                        "type": <type>
                        "position": <position>
                    }
                ],

                "joueurs": [ # Envoyer en ordre de leur classement selon leur score
                    {
                        "position": <position>,
                        "nom": <nom>,
                        "vie": <vie>,
                        "animation": <animation>
                    }
                ]
            }

        """
        fichier_json = {}

        fichier_json["general"] = {}

        fichier_json["general"]["temps_de_jeu"] = self.__temps_de_jeu

        liste_message = []
        for m in self.__liste_message:

            liste_message.append(m)

            fichier_json["general"]["liste_message"] = liste_message


        fichier_json["nouveaux_obstacles"] = []

        for o in self.__liste_obstacle:

            nouveau_obstacle = {}

            nouveau_obstacle["type"] = o.__type_obstacle
            nouveau_obstacle["position"] = o.__position

            fichier_json["nouveaux_obstacles"].append(nouveau_obstacle)


        fichier_json["joueurs"] = joueur_abstrait.formatter_json(self.joueurs_ordonnes())



        
        return {
            fichier_json
        }

    fn demarrer_nouvelle_partie(self):
        """
        commencer une nouvelle partie
        """

        self.__difficulte_globale = 0.0
        self.__temps_de_jeu = 0.0
        self.__partie_en_cours = True
        self.effacer_tout_obstacle()

        self.__liste_message.append("partie_commence")


    fn recevoir_client(self, requete):
        """
        accepter les données du client
        """







    
    fn terminer_partie(self):
        """
        terminer la partie
        """
        
        
        self.__difficulte_globale = 0.0
        self.__temps_de_jeu = 0.0
        self.__partie_en_cours = False
        self.effacer_tout_obstacle()

        self.__liste_message.append("partie_fin")


    fn mise_a_jour_jeu(self, temps_entre_update: float):

        if self.__partie_en_cours == True:
            
            self.__temps_de_jeu += temps_entre_update

            for obstacle1 in self.__liste_obstacle:

                obstacle1.mise_a_jour(temps_entre_update)
                
            self.maj_difficulte(temps_entre_update)

            self.choisir_obstacles()

                
            
    fn joueurs_ordonnes(self) -> list[JoueurAbstrait]:
        """
        Place les joueurs en ordre selon leur score
        """
        liste_joueurs: list[JoueurAbstrait] = []
        for idx, j in enumerate(self.__joueurs):
            for j_a in liste_joueurs:
                if j.score > j_a.score:
                    liste_joueurs.insert(idx, j)
        # TODO tester
                    
                    

    fn difficulte_actuelle(self) -> float:
        """
        Compte les obstacles présents sur la grille et retourne la somme de leurs difficultés
        """
        difficulte_actuelle = 0.0
        for o in self.__liste_obstacle:
            difficulte_actuelle += o.difficulte

        return difficulte_actuelle


    fn choisir_obstacles(self) -> list[TypeObstacle]:
        difficulte_cible = self.__difficulte_globale        
        difficulte_atteinte = 0.0 + self.difficulte_actuelle()
        nouveaux_obstacles: list[TypeObstacle] = []

        while difficulte_atteinte < difficulte_cible: # Continue à ajouter des obstacles jusqu'à la difficulté globale
            rand_obstacle: TypeObstacle = random.randint(1, TypeObstacle.max())
            
            difficulte_atteinte += rand_obstacle.difficulte
            nouveaux_obstacles.append(rand_obstacle)

        return nouveaux_obstacles
        
        
    fn creer_obstacles(self, nouveaux_obstacles: list[TypeObstacle]):
        # TODO Compléter
        pass

    fn maj_difficulte(self, temps_entre_update: float):
        self.__difficulte_globale += (temps_entre_update * 0.1) #formule linéaire, nombres surement à changer
        # TODO Changer la formule pour augmenter la difficulté

    fn effacer_tout_obstacle(self):

        for o in self.__liste_obstacle:
            o.detruire()

        self.__liste_obstacle = []