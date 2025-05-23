from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from services.loja_virtual import loja_virtual
from controllers import handle_error

router_vitrine = APIRouter()


@router_vitrine.get("/vitrine")
async def exibir_vitrine(session: AsyncSession = Depends(get_session)):
    return await loja_virtual.exibir_vitrine(session)


@router_vitrine.get("/vitrine/{cupcake_id}")
async def exibir_detalhes(
    cupcake_id: int, session: AsyncSession = Depends(get_session)
):
    try:
        return await loja_virtual.exibir_detalhes(cupcake_id, session)
    except Exception as e:
        handle_error(e)
