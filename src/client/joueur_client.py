from ursina.prefabs.first_person_controller import FirstPersonController
import client_serveur
import time
import json

class JoueurClient(FirstPersonController):
    def __init__(self, client: client_serveur.Client, height=2, **kwargs):
        super().__init__(height, **kwargs)
        self.__client = client
        self.__dernier_temps = self.__obtenir_temps()

    def __obtenir_temps(self) -> float:
        return time.time()

    def __emballer_les_donnees(self) -> str:
        return json.dumps({
            "Position": [
                self.position.x,
                self.position.y,
                self.position.z
            ]
        })
    
    def update(self):
        super().update()
        temps_en_ce_moment = self.__obtenir_temps()
        if temps_en_ce_moment - self.__dernier_temps > 1 / 12:
            self.__client.envoyer_message(self.__emballer_les_donnees())