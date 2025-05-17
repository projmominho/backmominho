import asyncio
from db import engine, Base

from models.cupcake import Cupcake


async def create_tables():
    print("Criando as tabelas no banco de dados...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Tabelas criadas com sucesso!")
