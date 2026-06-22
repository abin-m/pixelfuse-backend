from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pixelfuse.api.routes import convert, extract
from pixelfuse.config import Settings, get_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    cfg = settings or get_settings()
    app = FastAPI(
        title="PixelFuse API",
        description="Embed images into portable text files and extract them back.",
        version="1.0.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cfg.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(convert.router)
    app.include_router(extract.router)
    return app


app = create_app()
