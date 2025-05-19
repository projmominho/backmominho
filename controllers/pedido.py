from fastapi import APIRouter, Depends
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from services.pedido import pedido_service
from controllers import handle_error
from mytwilio import envia_sms


router_pedido = APIRouter()


# cria um novo pedido, faz um novo status e envia um sms com o numero
@router_pedido.post("/pedido-iniciar")
async def pedido_iniciar(
    pedido_json: dict, session: AsyncSession = Depends(get_session)
):
    telefone = pedido_json.get("phone")
    endereco = pedido_json.get("address")
    itens = pedido_json.get("cart")
    pedido = await pedido_service.novo(session, telefone, endereco, itens)
    envia_sms(
        to=telefone,
        mensagem=f"MOMINHO: Pedido {pedido.id} criado!",
    )

    return {"message": "Pedido criado com sucesso!", "pedido_id": pedido.id}


# Retorna o resumo do pedido (itens, totais, endereço, telefone) para exibir na confirmação/finalização.
@router_pedido.get("/pedido-resumo/{pedido_id}")
async def exibir_resumo(pedido_id: int, session: AsyncSession = Depends(get_session)):
    try:
        return await pedido_service.exibir_resumo(pedido_id, session)
    except Exception as e:
        handle_error(e)
