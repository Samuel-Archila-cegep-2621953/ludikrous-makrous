import asyncio

CONFIGURATION_CLIENT = {
    "IP": '127.0.0.1',
    "Port": 24113
}

class Client:
    def __init__(self):
        pass
    async def gerer_envoyer_message(self, message: str) -> str:
        _message = await self.__envoyer_message(message)
        await self.__fermer()
        return _message
    
    async def __envoyer_message(self, message: str) -> str:
        self.__lire, self.__ecrire = await asyncio.open_connection(CONFIGURATION_CLIENT["IP"], CONFIGURATION_CLIENT["Port"])

        self.__ecrire.write(message.encode('utf-8'))
        await self.__ecrire.drain()

        donnee = await self.__lire.read(4096)
        return donnee.decode('utf-8')

    async def __fermer(self):
        self.__ecrire.close()
        await self.__ecrire.wait_closed()

    def envoyer_message(self, message: str) -> str:
        return asyncio.run(self.gerer_envoyer_message(message))