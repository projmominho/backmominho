from dotenv import load_dotenv

load_dotenv()

from setup.create_app import create_app
from setup.create_tables import create_tables

app = create_app()


# Rodar a criação das tabelas ao iniciar o FastAPI
@app.on_event("startup")
async def on_startup():
    await create_tables()
