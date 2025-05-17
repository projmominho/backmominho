from db import fetch_all, objects_to_json

from models.cupcake import Cupcake


class LojaVirtual:

    def __init__(self):
        self.lista_cupcakes = None

    # busca cupcakes na memória primeiro senão ter busca no banco, retorna JSON
    async def exibirVitrine(self, session):
        if self.lista_cupcakes is not None:
            return objects_to_json(self.lista_cupcakes)

        cupcakes = await fetch_all(session, Cupcake)
        self.lista_cupcakes = cupcakes
        return objects_to_json(cupcakes)


# cria instância única para evitar conflitos
loja_virtual = LojaVirtual()
