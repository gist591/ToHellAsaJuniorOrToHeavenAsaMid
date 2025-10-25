FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    python3-dev \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml LICENSE README.md ./

RUN pip install --no-cache-dir uv && \
    uv sync --no-dev

COPY . /app

RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

CMD ["uv", "run", "uvicorn", "to_the_hell.oncallhub.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
