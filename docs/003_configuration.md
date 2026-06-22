# Configuration

All settings are read from environment variables prefixed `PIXELFUSE_`. A `.env` file in the project root is loaded automatically.

| Variable | Default | Description |
|----------|---------|-------------|
| `PIXELFUSE_HOST` | `0.0.0.0` | Bind host |
| `PIXELFUSE_PORT` | `8000` | Bind port |
| `PIXELFUSE_LOG_LEVEL` | `info` | Uvicorn log level |
| `PIXELFUSE_MAX_UPLOAD_FILES` | `10` | Max files per `/convert-embed/` request |
| `PIXELFUSE_ALLOWED_ORIGINS` | *(required)* | JSON array of CORS origins, e.g. `["http://localhost:3000"]` |

Copy `.env.example` to `.env` and fill in `PIXELFUSE_ALLOWED_ORIGINS` before running locally.

CLI flags (`--host`, `--port`, `--log-level`) override env vars when passed to `pixelfuse serve`.
