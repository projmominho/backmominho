from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.cupcake import Cupcake
from services.loja_virtual import loja_virtual


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


admin_service = AdminService()
