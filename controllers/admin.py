import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from controllers import handle_error
from services.admin import admin_service

router_admin = APIRouter()

ADMIN_KEY = os.getenv("ADMIN_KEY")


class AdminConnectRequest(BaseModel):
    key: str


def verificar_admin_key(chave: str):
    if chave != ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Acesso Negado")


@router_admin.post("/admin-connect")
async def admin_connect(data: AdminConnectRequest):
    try:
        verificar_admin_key(data.key)
        return True
    except Exception as e:
        handle_error(e)


@router_admin.post("/admin-cupcakes")
async def exibir_cupcakes(
    data: AdminConnectRequest, session: AsyncSession = Depends(get_session)
):
    try:
        verificar_admin_key(data.key)
        return await admin_service.exibir_cupcakes(session)
    except Exception as e:
        handle_error(e)


@router_admin.post("/admin-editar-cupcake")
async def admin_editar_cupcake(
    data: dict, session: AsyncSession = Depends(get_session)
):
    verificar_admin_key(data["key"])
    print(data)

    return await admin_service.editar_cupcake(
        session,
        id=data["id"],
        nome=data["nome"],
        preco=data["preco"],
        disponibilidade=data["disponibilidade"],
    )


@router_admin.post("/admin-pedidos")
async def exibir_pedidos(
    data: AdminConnectRequest, session: AsyncSession = Depends(get_session)
):
    try:
        verificar_admin_key(data.key)
        return await admin_service.listar_pedidos(session)
    except Exception as e:
        handle_error(e)


@router_admin.put("/admin-update-status")
async def admin_update_status(data: dict, session: AsyncSession = Depends(get_session)):
    try:
        verificar_admin_key(data["key"])
        return await admin_service.atualizar_status(
            session, pedido_id=data["id"], status=data["status"]
        )
    except Exception as e:
        handle_error(e)
