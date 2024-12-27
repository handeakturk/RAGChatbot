from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.services.middleware import log_requests
from app.routers import search
from app.configs.logger.logging import logger


def configure_middlewares(app: FastAPI) -> None:


    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Her yerden gelen isteklere izin ver
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.middleware("http")(log_requests)


def init_routers(app: FastAPI) -> None:
    app.include_router(search.router)


def create_app() -> FastAPI:
    app = FastAPI()
    configure_middlewares(app)
    init_routers(app)

    return app 

app = create_app()
