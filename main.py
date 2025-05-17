from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from create_tables import create_tables
import os
from dotenv import load_dotenv
from routers import routers

import asyncio

load_dotenv()

allowed_origins = os.getenv("CORS_ALLOWED_ORIGINS").split(",")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routers:
    app.include_router(router)


# Rodar a criação das tabelas ao iniciar o FastAPI
@app.on_event("startup")
async def on_startup():
    await create_tables()
