from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from services.loja_virtual import loja_virtual

router_vitrine = APIRouter()


@router_vitrine.get("/vitrine")
async def exibir_vitrine(session: AsyncSession = Depends(get_session)):
    return await loja_virtual.exibir_vitrine(session)
