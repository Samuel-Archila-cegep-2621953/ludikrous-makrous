import asyncio
import tomllib
from pathlib import Path
from config import Config
from paquet import *
import type_paquet
from type_paquet import TypePaquetServeur
import time
from type_obstacle import TypeObstacle
from debogage import Debogage as Dbg

class Client:
    def __init__(self):
        self.__config = Config.json()
        Dbg.info(self.__config, 3)

    async def __gerer_envoyer_message(self, message: str) -> dict:
        _message: list[tuple[TypePaquetServeur, bytes]] = await self.__envoyer_message(message)
        await self.__fermer()
        Dbg.info(f"DANS client_serveur::__gerer_envoyer_message: Msg recv: {_message}", 5)
        _decode: dict[str, any] = deconstruire_superpaquet(_message)
        Dbg.info(_decode, 5)
        return _decode

    async def __gerer_envoyer_message_bas(self, message: str) -> str:
        self.__lire, self.__ecrire = await asyncio.open_connection(self.__config["Client"]["ip"], self.__config["Client"]["port"])
        self.__ecrire.write(message.encode())
        await self.__ecrire.drain()

        _texte = await self.__lire.read()
        _resultat = _texte.decode()

        return _resultat
    
    async def __envoyer_message(self, message: bytes) -> list[tuple[TypePaquetServeur, bytes]]:
        self.__lire, self.__ecrire = await asyncio.open_connection(self.__config["Client"]["ip"], self.__config["Client"]["port"])

        #self.__ecrire.write(message.encode('utf-8'))

        #print(f"MESSAGE ENVOYÉ: {message}")

        self.__ecrire.write(message)
        await self.__ecrire.drain()

        # SECTION RECEVOIR MESSAGE

        _aw_nb_paquets = await self.__lire.readexactly(2) # Lire le nombre de paquets
        _nb_paquets = struct.unpack('!H', _aw_nb_paquets)[0] # u16
        Dbg.info(f"Le nombre de paquets dans le superpaquet dans __ENVOYER_MESSAGE EST: {_nb_paquets}", 2)

        _liste_paquets: list[tuple[TypePaquetServeur, bytes]] = []

        for _ in range(_nb_paquets):
            _entete = await self.__lire.readexactly(1) # Lire l'en-tête pour déterminer le type de paquet
            _type_paquet: int = struct.unpack('!B', _entete)[0] # u8, est un tuple duquel il faut extraire la valeur
            _repack_type_obstacle: bytes = None

            if _type_paquet > TypePaquetServeur.max(): _type_paquet = 0 #HACK Ignore / remplace les paquets >= 61

            Dbg.info(f"Le type de paquet dans __ENVOYER_MESSAGE EST: {_type_paquet}", 3)

            _longueur_message: int = longueur_paquet(_type_paquet)


            if _type_paquet == TypePaquetServeur.MAJ_OBSTACLE.value:
                Dbg.info("OBSTACLES REçUS!", 2)
                _bytes_type_obstacle: bytes = await self.__lire.readexactly(1) # u8 indiquant le type d'obstacle
                _type_obstacle: int = struct.unpack('!B', _bytes_type_obstacle)[0] # Se rappeler que c'est un tuple contenant un seul u8

                """
                if _type_obstacle == TypeObstacle.TRAIN.value:
                    _bytes_longueur_train: bytes = await self.__lire.readexactly(1) 
                    _longueur_train: int = struct.unpack('!B', _bytes_longueur_train)[0] # Le train a une longueur variable
                    _longueur_message: int = 2 + 2 * _longueur_train # Pour chaque longueur_train_u, lire 2 octets (coord x y) + 2 (Coord initiale x y)

                    _repack_type_obstacle = _bytes_type_obstacle + _bytes_longueur_train
                """
                #else:
                #NOTE TEST 
                _longueur_message += TypeObstacle.nb_bytes(_type_obstacle) - 1 # Enlever 1 pour l'entête de type obstacle qui a déjà été lue
                _repack_type_obstacle = _bytes_type_obstacle

            
            _ce_paquet: bytes = await self.__lire.readexactly(_longueur_message)

            if _repack_type_obstacle is not None: # Rattacher le type d'obstacle pour plus tard, car sinon _ce_paquet contiendrait seulement des octets d'obstacle sans le type d'obstacle
                _ce_paquet = _repack_type_obstacle + _ce_paquet

            _liste_paquets.append((
                TypePaquetServeur.depuis_int(_type_paquet),
                _ce_paquet
            ))

        # BUG Je ne pense pas que ce code fait quelque chose. Je le lasse pour le moment au cas ou c'était important
        """
        print(f"LEN MSG EXPECT {_longueur_message}")
        try: 
            donnee = await self.__lire.readexactly(_longueur_message)
        except Exception as e:
            print(f"ERREUR DANS __ENVOYER_MESSAGE: {e}")
            print(time.time())
            #exit(1)
        """


        #print("\033[91mDonnees lues" + str(donnee))
        return _liste_paquets

    async def __fermer(self):
        self.__ecrire.close()
        await self.__ecrire.wait_closed()

    def envoyer_message(self, message: bytes) -> dict:
        return asyncio.run(self.__gerer_envoyer_message(message))

    def envoyer_message_bas(self, message: str) -> str:
        return asyncio.run(self.__gerer_envoyer_message_bas(message))

