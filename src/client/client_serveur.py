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
    
    async def __envoyer_message(self, message: bytes) -> list[tuple[TypePaquetServeur, bytes]]:
        # Retourne la réponse?
        self.__lire, self.__ecrire = await asyncio.open_connection(self.__config["Client"]["ip"], self.__config["Client"]["port"])

        #self.__ecrire.write(message.encode('utf-8'))
        print(f"MESSAGE IN __ENVOYER_MESsAGE: {message}")
        self.__ecrire.write(message)
        await self.__ecrire.drain()


        _aw_nb_paquets = await self.__lire.readexactly(2) # Lire le nombre de paquets
        _nb_paquets = struct.unpack('H', _aw_nb_paquets)[0] # BIG ENDIAN u16

        _liste_paquets: list[tuple[TypePaquetServeur, bytes]] = []

        for _ in range(_nb_paquets):
            _entete = await self.__lire.readexactly(1) # Lire l'en-tête pour déterminer le type de paquet
            _type_paquet: int = struct.unpack('B', _entete) # u8
            _longueur_message: int = longueur_paquet(_entete)
            
            _ce_paquet = await self.__lire.readexactly(_longueur_message)
            _liste_paquets.append((
                TypePaquetServeur.depuis_int(_type_paquet),
                _ce_paquet
            ))

        print(f"LEN MSG EXPECT {_longueur_message}")
        try: 
            donnee = await self.__lire.readexactly(_longueur_message)
        except Exception as e:
            print(f"EXCEPT DANS __ENVOYER_MESSAGE: {e}")
            print(time.time())
            exit()


        print("\033[91mDonnees lues" + str(donnee))
        #NOTE Vieuxreturn donnee.decode('utf-8')
        return _liste_paquets

    async def __fermer(self):
        self.__ecrire.close()
        await self.__ecrire.wait_closed()

    #NOTE VIEUX def envoyer_message(self, message: bytes) -> str:
    def envoyer_message(self, message: bytes) -> dict:
        return asyncio.run(self.__gerer_envoyer_message(message))

