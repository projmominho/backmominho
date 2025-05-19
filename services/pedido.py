from models.pedido import Pedido, PedidoStatus, PedidoItem
from models.cupcake import Cupcake
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from services.service_error import ServiceError
from datetime import datetime


class PedidoService:
    def __init__(self):
        pass

    # Cria um novo pedido e adiciona os itens
    async def novo(self, session, telefone, endereco, itens):
        try:
            pedido = Pedido(telefone=telefone, endereco=endereco, valor_pago=0.0)
            session.add(pedido)
            await session.flush()

            for item in itens:
                novo_item = PedidoItem(
                    cupcake_id=item["id"],
                    quantidade=item["quantidade"],
                    observacoes=item.get("observacoes", ""),
                    pedido_id=pedido.id,
                )
                session.add(novo_item)

            status = PedidoStatus(
                pedido_id=pedido.id,
                status="pedido_iniciado",
                data_status=datetime.utcnow(),
            )
            session.add(status)

            await session.commit()
            await session.refresh(pedido)
            return pedido
        except SQLAlchemyError as e:
            await session.rollback()
            raise ServiceError(
                payload={"message": "Erro ao criar pedido", "status_code": 500}
            )

    # Atualiza o status do pedido (adiciona uma linha em pedido_status)
    async def atualizar_status(self, session, pedido_id, novo_status):
        try:
            status = PedidoStatus(
                pedido_id=pedido_id, status=novo_status, data_status=datetime.utcnow()
            )
            session.add(status)
            await session.commit()
            return status
        except SQLAlchemyError:
            await session.rollback()
            raise ServiceError(
                payload={"message": "Erro ao atualizar status", "status_code": 500}
            )

    # Atualiza o valor_pago do pedido (pagamento realizado)
    async def realizar_pagamento(self, session, pedido_id, valor_pago):
        try:
            query = select(Pedido).where(Pedido.id == pedido_id)
            result = await session.execute(query)
            pedido = result.scalar_one_or_none()
            if not pedido:
                raise ServiceError(
                    payload={"message": "Pedido não encontrado", "status_code": 404}
                )
            pedido.valor_pago = valor_pago
            await session.commit()
            await session.refresh(pedido)
            return pedido
        except SQLAlchemyError:
            await session.rollback()
            raise ServiceError(
                payload={"message": "Erro ao realizar pagamento", "status_code": 500}
            )

    # Busca os dados do pedido, itens e monta o resumo para exibição.
    async def exibir_resumo(self, pedido_id: int, session):
        pedido = await session.get(Pedido, pedido_id)
        print("Pedido:", pedido)

        if not pedido:
            raise ServiceError(
                payload={"message": "Pedido não encontrado", "status_code": 500}
            )

        query = (
            select(PedidoItem, Cupcake)
            .join(Cupcake, PedidoItem.cupcake_id == Cupcake.id)
            .where(PedidoItem.pedido_id == pedido_id)
        )
        result = await session.execute(query)
        itens = []
        valor_total = 0

        for pedido_item, cupcake in result:
            subtotal = pedido_item.quantidade * cupcake.preco
            valor_total += subtotal
            itens.append(
                {
                    "nome": cupcake.nome,
                    "quantidade": pedido_item.quantidade,
                    "valor_unitario": cupcake.preco,
                    "subtotal": subtotal,
                }
            )

        resumo = {
            "telefone": pedido.telefone,
            "endereco": pedido.endereco,
            "valor_pago": pedido.valor_pago,
            "itens": itens,
            "valor_total": valor_total,
        }
        return resumo


pedido_service = PedidoService()
