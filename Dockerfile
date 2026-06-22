FROM python:3.11-slim AS builder

WORKDIR /build

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY pyproject.toml README.md ./
COPY src/ src/

RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir .


FROM python:3.11-slim

RUN useradd --create-home --shell /bin/bash app

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH" \
    PIXELFUSE_HOST=0.0.0.0 \
    PIXELFUSE_PORT=8000 \
    PIXELFUSE_LOG_LEVEL=info

WORKDIR /app
USER app

EXPOSE 8000

CMD ["uvicorn", "pixelfuse.main:app", "--host", "0.0.0.0", "--port", "8000"]
