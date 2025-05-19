from db import fetch_all, objects_to_json
from services.service_error import ServiceError

from models.cupcake import Cupcake


class LojaVirtual:

    def __init__(self):
        self.lista_cupcakes = None

    # busca cupcakes na memória primeiro senão ter busca no banco, retorna JSON
    async def exibir_vitrine(self, session):
        if self.lista_cupcakes is not None:
            return objects_to_json(self.lista_cupcakes)

        cupcakes = await fetch_all(session, Cupcake)
        self.lista_cupcakes = cupcakes
        return objects_to_json(
            cupcakes,
            campos=[
                Cupcake.id,
                Cupcake.nome,
                Cupcake.descricao,
                Cupcake.preco,
                Cupcake.disponibilidade,
                Cupcake.imagem,
            ],
        )

    # Busca o cupcake pelo id na memória ou no banco e retorna os detalhes
    async def exibir_detalhes(self, cupcake_id, session):
        if self.lista_cupcakes is not None:
            cupcake = next(
                filter(lambda c: c.id == cupcake_id, self.lista_cupcakes), None
            )
        else:
            cupcake = await session.get(Cupcake, cupcake_id)

        if cupcake is None:
            raise ServiceError(
                payload={"message": "bolinho não encontrado", "status_code": 404}
            )

        campos = [
            Cupcake.id,
            Cupcake.nome,
            Cupcake.descricao,
            Cupcake.ingredientes,
            Cupcake.peso,
            Cupcake.dimensoes,
            Cupcake.informacoes_nutricionais,
            Cupcake.preco,
            Cupcake.disponibilidade,
            Cupcake.imagem,
        ]
        return objects_to_json([cupcake], campos=campos)[0]


# cria instância única para evitar conflitos
loja_virtual = LojaVirtual()
