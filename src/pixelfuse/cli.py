from typing import Optional

import typer
import uvicorn

from pixelfuse.config import get_settings

cli = typer.Typer(name="pixelfuse", help="PixelFuse — image embedding API server.")


@cli.command()
def serve(
    host: Optional[str] = typer.Option(None, help="Bind host (overrides PIXELFUSE_HOST)"),
    port: Optional[int] = typer.Option(None, help="Bind port (overrides PIXELFUSE_PORT)"),
    reload: bool = typer.Option(False, "--reload", help="Enable auto-reload (dev only)"),
    log_level: Optional[str] = typer.Option(
        None, help="Log level (overrides PIXELFUSE_LOG_LEVEL)"
    ),
) -> None:
    cfg = get_settings()
    uvicorn.run(
        "pixelfuse.main:app",
        host=host or cfg.host,
        port=port or cfg.port,
        log_level=log_level or cfg.log_level,
        reload=reload,
    )


if __name__ == "__main__":
    cli()
