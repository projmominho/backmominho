from fastapi import FastAPI
from cupcake import router as cupcake_router

app = FastAPI()

app.include_router(cupcake_router)
