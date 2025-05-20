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
    try:
        telefone = pedido_json.get("phone")
        endereco = pedido_json.get("address")
        itens = pedido_json.get("cart")
        pedido = await pedido_service.novo(session, telefone, endereco, itens)
        envia_sms(
            to=telefone,
            mensagem=f"MOMINHO: Pedido #{pedido.id} criado!",
        )

        return {"message": "Pedido criado com sucesso!", "pedido_id": pedido.id}
    except Exception as e:
        handle_error(e)


# Retorna o resumo do pedido (itens, totais, endereço, telefone) para exibir na confirmação/finalização.
@router_pedido.post("/pedido-resumo")
async def exibir_resumo(payload: dict, session: AsyncSession = Depends(get_session)):
    try:
        pedido_id = int(payload.get("id"))
        telefone = str(payload.get("telefone"))
        return await pedido_service.exibir_resumo(pedido_id, telefone, session)
    except Exception as e:
        handle_error(e)


# Retorna o histórico de status do pedido
@router_pedido.post("/pedido-status")
async def pedido_status(payload: dict, session: AsyncSession = Depends(get_session)):
    try:
        pedido_id = int(payload.get("id"))
        telefone = str(payload.get("telefone"))
        return await pedido_service.exibir_status(session, pedido_id, telefone)
    except Exception as e:
        handle_error(e)
