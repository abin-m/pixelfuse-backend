# Deployment

## Render

The service is configured for [Render](https://render.com) via `render.yaml`. On every push to `main`:

1. Render builds the Docker image from `Dockerfile`.
2. The container starts with `pixelfuse serve`.
3. Set `PIXELFUSE_ALLOWED_ORIGINS` in the Render environment dashboard.

## CI

GitHub Actions runs lint, type check, and tests on every push and pull request to `main`. See `.github/workflows/ci.yml`.

## Docker (self-hosted)

```bash
docker build -t pixelfuse .
docker run -p 8000:8000 \
  -e PIXELFUSE_ALLOWED_ORIGINS='["https://yourdomain.com"]' \
  pixelfuse
```
