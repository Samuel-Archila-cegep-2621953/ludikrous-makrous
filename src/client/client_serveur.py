import asyncio
import tomllib
from pathlib import Path
from config import Config
from paquet import *
import type_paquet
from type_paquet import TypePaquetServeur
import time

class Client:
    def __init__(self):
        _fichier_toml = open(Path(__file__).parent / "config.toml", 'rb')
        self.__config = Config.json()
        #self.__config = tomllib.load(_fichier_toml)

    #NOTE VIEUX async def __gerer_envoyer_message(self, message: str) -> str:
    async def __gerer_envoyer_message(self, message: str) -> dict:
        _message = await self.__envoyer_message(message)
        await self.__fermer()
        return _message
    
    async def __envoyer_message(self, message: bytes) -> dict:
        # Retourne la réponse?
        try:
            self.__lire, self.__ecrire = await asyncio.open_connection(self.__config["Client"]["ip"], self.__config["Client"]["port"])
        except Exception as e:
            print(f"ERREUR CONNEXION ASYNCIO>OPEN{e}")

        #self.__ecrire.write(message.encode('utf-8'))
        print(f"MESSAGE IN __ENVOYER_MESsAGE: {message}")
        self.__ecrire.write(message)
        await self.__ecrire.drain()


        _aw_nb_paquets = await self.__lire.readexactly(1) # LIre le type
        _nb_paquets = struct.unpack('H', _aw_nb_paquets) # BIG ENDIAN

        for i in range(_nb_paquets):
            _longueur_message: int = longueur(_entete)
            #TODO CREER LA LISTE DE PAQUETS

        print(f"LEN MSG EXPECT {_longueur_message}")
        try: 
            donnee = await self.__lire.readexactly(_longueur_message)
        except Exception as e:
            print(f"EXCEPT DANS __ENVOYER_MESSAGE: {e}")
            print(time.time())
            exit()

        self.__ecrire.close()
        await self.__ecrire.wait_closed()

        print("\033[91mDonnees lues" + str(donnee))
        #NOTE Vieuxreturn donnee.decode('utf-8')
        return interpreter_paquet(lire_paquet(donnee))

    async def __fermer(self):
        self.__ecrire.close()
        await self.__ecrire.wait_closed()

    #NOTE VIEUX def envoyer_message(self, message: bytes) -> str:
    def envoyer_message(self, message: bytes) -> dict:
        return asyncio.run(self.__gerer_envoyer_message(message))

