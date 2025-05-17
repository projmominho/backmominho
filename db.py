import os
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do .env (localmente)
load_dotenv()

# Monta a URL de conexão com o PostgreSQL no formato async
DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Cria a engine assíncrona
engine = create_async_engine(DATABASE_URL, echo=True)

# Cria o "Base" para as classes dos models herdarem
Base = declarative_base()

# Cria um sessionmaker para gerar sessões assíncronas
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,  # Define que a session será assíncrona
    expire_on_commit=False,
)


# fornece uma sessão com o banco para cada request (padrão do FastAPI)
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


# retorna todos os resultados de um model
async def fetch_all(session, model):
    resultado = await session.execute(select(model))
    registros = resultado.scalars().all()
    return registros


# converte uma lista de objetos sqlalchemy em lista de dicts/json
# se campos for passado, espera lista de atributos do model (ex: [Cupcake.id, Cupcake.nome]).
def objects_to_json(registros, campos=None):
    if campos is None:
        return [
            {column.name: getattr(r, column.name) for column in r.__table__.columns}
            for r in registros
        ]
    nomes_campos = [campo.name for campo in campos]
    return [{campo: getattr(r, campo) for campo in nomes_campos} for r in registros]
