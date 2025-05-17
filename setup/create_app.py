from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.routers import routers
import os


def create_app() -> FastAPI:
    app = FastAPI()

    allowed_origins = os.getenv("CORS_ALLOWED_ORIGINS").split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for router in routers:
        app.include_router(router)

    return app
