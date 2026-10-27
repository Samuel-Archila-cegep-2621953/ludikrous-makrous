import asyncio
import tomllib
from pathlib import Path
from config import Config

class Client:
    def __init__(self):
        _fichier_toml = open(Path(__file__).parent / "config.toml", 'rb')
        self.__config = Config.json()
        #self.__config = tomllib.load(_fichier_toml)

    async def __gerer_envoyer_message(self, message: str) -> str:
        _message = await self.__envoyer_message(message)
        await self.__fermer()
        return _message
    
    async def __envoyer_message(self, message: str) -> str:
        self.__lire, self.__ecrire = await asyncio.open_connection(self.__config["Client"]["ip"], self.__config["Client"]["port"])

        self.__ecrire.write(message.encode('utf-8'))
        await self.__ecrire.drain()

        donnee = await self.__lire.read(4096)
        return donnee.decode('utf-8')

    async def __fermer(self):
        self.__ecrire.close()
        await self.__ecrire.wait_closed()

    def envoyer_message(self, message: str) -> str:
        return asyncio.run(self.__gerer_envoyer_message(message))

