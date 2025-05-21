from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from models.cupcake import Cupcake
from models.pedido import Pedido, PedidoStatus
from services.loja_virtual import loja_virtual
from mytwilio import whats_pedido_atualizado


class AdminService:
    # retorna todos os cupcakes cadastrados.
    async def exibir_cupcakes(self, session: AsyncSession):
        result = await session.execute(select(Cupcake).order_by(Cupcake.id.asc()))
        return result.scalars().all()

    async def editar_cupcake(
        self,
        session: AsyncSession,
        id: int,
        nome: str,
        preco: float,
        disponibilidade: bool,
    ):
        result = await session.execute(select(Cupcake).where(Cupcake.id == id))
        cupcake = result.scalar_one_or_none()

        if not cupcake:
            raise ServiceError(
                payload={"message": "bolinho não encontrado", "status_code": 404}
            )

        cupcake.nome = nome
        cupcake.preco = preco
        cupcake.disponibilidade = disponibilidade

        await loja_virtual.atualizar_lista_cupcakes(session=session)

        await session.commit()
        await session.refresh(cupcake)

        return {"ok": True, "message": "Cupcake atualizado com sucesso"}

    async def listar_pedidos(self, session: AsyncSession):
        result = await session.execute(
            select(Pedido)
            .options(selectinload(Pedido.status))
            .order_by(Pedido.id.asc())
        )
        pedidos = result.scalars().all()

        lista = []

        for pedido in pedidos:
            ultimo_status = None
            if pedido.status:
                ultimo_status = sorted(
                    pedido.status, key=lambda s: s.data_status, reverse=True
                )[0].status

            lista.append(
                {
                    "id": pedido.id,
                    "telefone": pedido.telefone,
                    "endereco": pedido.endereco,
                    "valor_pago": pedido.valor_pago,
                    "status": ultimo_status or "sem status",
                }
            )

        return lista

    async def atualizar_status(
        self, session: AsyncSession, pedido_id: int, status: str
    ):
        result = await session.execute(select(Pedido).where(Pedido.id == pedido_id))
        pedido = result.scalar_one_or_none()

        if not pedido:
            raise ServiceError(
                payload={"message": "Pedido não encontrado", "status_code": 404}
            )

        novo_status = PedidoStatus(pedido_id=pedido.id, status=status)

        session.add(novo_status)
        await session.commit()
        await session.refresh(novo_status)

        whats_pedido_atualizado(
            to=pedido.telefone, codigo_pedido=f"{pedido_id}?telefone={pedido.telefone}"
        )

        return {"ok": True, "message": "Status atualizado com sucesso"}


admin_service = AdminService()
