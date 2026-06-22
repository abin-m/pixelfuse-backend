# PixelFuse Backend

FastAPI service that embeds images into portable text files and extracts them back.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/convert-embed/` | Upload images → download base64 text file |
| POST | `/extract-images/` | Upload text file → download ZIP of images |

Supports JPEG, PNG, and HEIC formats. Max 10 files per request (configurable).

## Quickstart

```bash
pip install -e ".[dev]"
pixelfuse serve --reload
```

## Configuration

All settings are overridable via environment variables prefixed `PIXELFUSE_`:

| Variable | Default | Description |
|----------|---------|-------------|
| `PIXELFUSE_HOST` | `0.0.0.0` | Bind host |
| `PIXELFUSE_PORT` | `8000` | Bind port |
| `PIXELFUSE_LOG_LEVEL` | `info` | Uvicorn log level |
| `PIXELFUSE_MAX_UPLOAD_FILES` | `10` | Max files per request |
| `PIXELFUSE_ALLOWED_ORIGINS` | `["https://pixelfuse-frontend.onrender.com"]` | CORS origins (JSON array) |

Copy `.env.example` to `.env` for local overrides.

## Development

```bash
# Lint
ruff check src tests

# Test
pytest --tb=short
```

## Deployment

Deployed on [Render](https://render.com) via `render.yaml`. CI runs on every push via GitHub Actions.
