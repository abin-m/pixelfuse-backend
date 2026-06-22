import time
from collections import defaultdict

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

    _rate_store: dict[str, list[float]] = defaultdict(list)

    @app.middleware("http")
    async def security_middleware(request: Request, call_next: object) -> object:
        ip = request.client.host if request.client else "unknown"
        now = time.time()
        _rate_store[ip] = [t for t in _rate_store[ip] if now - t < 60]
        if len(_rate_store[ip]) >= cfg.rate_limit_per_minute:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Try again later."},
            )
        _rate_store[ip].append(now)

        if request.method in ("POST", "PUT", "PATCH"):
            total = 0
            chunks: list[bytes] = []
            async for chunk in request.stream():
                total += len(chunk)
                if total > MAX_UPLOAD_BYTES:
                    return JSONResponse(
                        status_code=413,
                        content={"detail": "Upload exceeds 20 MB limit."},
                    )
                chunks.append(chunk)
            request._body = b"".join(chunks)  # type: ignore[attr-defined]

        return await call_next(request)  # type: ignore[operator]

    app.include_router(convert.router)
    app.include_router(extract.router)
    return app


app = create_app()
