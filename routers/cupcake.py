from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db import get_session
from models.cupcake import Cupcake

cupcake_router = APIRouter()


@cupcake_router.get("/cupcakes")
async def listar_cupcakes(session: AsyncSession = Depends(get_session)):
    """
    Retorna a lista de todos os cupcakes cadastrados no banco de dados.
    """
    resultado = await session.execute(select(Cupcake))
    cupcakes = resultado.scalars().all()
    lista = []
    for c in cupcakes:
        lista.append(
            {
                "id": c.id,
                "nome": c.nome,
                "descricao": c.descricao,
                "preco": c.preco,
                "disponibilidade": c.disponibilidade,
                "ingredientes": c.ingredientes,
                "peso": c.peso,
                "dimensoes": c.dimensoes,
                "informacoes_nutricionais": c.informacoes_nutricionais,
                "imagem": c.imagem,
            }
        )
    return lista
