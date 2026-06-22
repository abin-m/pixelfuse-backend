from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from pixelfuse.api.routes import convert, extract
from pixelfuse.config import Settings, get_settings

MAX_UPLOAD_BYTES = 20 * 1024 * 1024  # 20 MB


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
        allow_credentials=False,
        allow_methods=["POST"],
        allow_headers=["Content-Type"],
    )

    @app.middleware("http")
    async def limit_upload_size(request: Request, call_next: object) -> object:
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > MAX_UPLOAD_BYTES:
            return JSONResponse(
                status_code=413,
                content={"detail": "Upload exceeds 20 MB limit."},
            )
        return await call_next(request)  # type: ignore[operator]

    app.include_router(convert.router)
    app.include_router(extract.router)
    return app


app = create_app()
