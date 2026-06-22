import argparse

import uvicorn

from pixelfuse.config import get_settings


def serve(args: argparse.Namespace) -> None:
    cfg = get_settings()
    uvicorn.run(
        "pixelfuse.main:app",
        host=args.host or cfg.host,
        port=args.port or cfg.port,
        log_level=args.log_level or cfg.log_level,
        reload=args.reload,
    )


def cli() -> None:
    parser = argparse.ArgumentParser(
        prog="pixelfuse",
        description="PixelFuse — image embedding API server.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    serve_cmd = sub.add_parser("serve", help="Start the API server.")
    serve_cmd.add_argument("--host", default=None, help="Bind host (overrides PIXELFUSE_HOST)")
    serve_cmd.add_argument("--port", type=int, default=None, help="Bind port (overrides PIXELFUSE_PORT)")
    serve_cmd.add_argument("--reload", action="store_true", help="Enable auto-reload (dev only)")
    serve_cmd.add_argument("--log-level", dest="log_level", default=None, help="Log level (overrides PIXELFUSE_LOG_LEVEL)")

    args = parser.parse_args()
    if args.command == "serve":
        serve(args)


if __name__ == "__main__":
    cli()
