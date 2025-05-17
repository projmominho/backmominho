from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from services.loja_virtual import loja_virtual

cupcake_router = APIRouter()


@cupcake_router.get("/cupcake")
async def listar_cupcakes(session: AsyncSession = Depends(get_session)):
    return await loja_virtual.exibirVitrine(session)
