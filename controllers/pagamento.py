from fastapi import APIRouter, Depends
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from controllers import handle_error
from services.pagamento import pagamento_service

router_pagamento = APIRouter()


# Endpoint de pagamento por cartão de crédito
@router_pagamento.post("/pagamento-cartao")
async def pagamento_cartao(
    pagamento_json: dict, session: AsyncSession = Depends(get_session)
):
    try:
        return await pagamento_service.pagamento_cartao(session, pagamento_json)
    except Exception as e:
        handle_error(e)


# Endpoint de pagamento por pix
@router_pagamento.post("/pagamento-pix")
async def pagamento_cartao(
    pagamento_json: dict, session: AsyncSession = Depends(get_session)
):
    try:
        return await pagamento_service.pagamento_pix(session, pagamento_json)
    except Exception as e:
        handle_error(e)
