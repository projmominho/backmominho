from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from cupcake import router as cupcake_router
import os
from dotenv import load_dotenv

load_dotenv()

# Obter as origens permitidas a partir da variável de ambiente
allowed_origins = os.getenv("CORS_ALLOWED_ORIGINS").split(",")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cupcake_router)
