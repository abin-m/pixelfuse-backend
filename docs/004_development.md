# Development

## Setup

```bash
pip install -e ".[dev]"
cp .env.example .env   # fill in PIXELFUSE_ALLOWED_ORIGINS
pixelfuse serve --reload
```

## Running tests

```bash
pytest
```

## Lint & type check

```bash
flake8 src tests
mypy src
```

Run all environments at once:

```bash
tox
```

## Docker

```bash
docker compose up --build
```

The compose file mounts `.env` automatically. The server is available at `http://localhost:8000`.

## Project layout

```
src/pixelfuse/
  api/routes/
    convert.py   # POST /convert-embed/
    extract.py   # POST /extract-images/
  cli.py         # pixelfuse serve entry point
  config.py      # pydantic-settings config
  main.py        # FastAPI app factory
tests/
  test_convert.py
  test_extract.py
```
