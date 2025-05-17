from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session, fetch_all
from models.cupcake import Cupcake

cupcake_router = APIRouter()


# Retorna a lista de todos os cupcakes cadastrados no banco de dados.
@cupcake_router.get("/cupcakes")
async def listar_cupcakes(session: AsyncSession = Depends(get_session)):
    return await fetch_all(session, Cupcake)
