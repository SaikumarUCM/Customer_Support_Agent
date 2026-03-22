FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency manifests first for layer caching
COPY pyproject.toml .
COPY README.md .

# Install production dependencies only
RUN uv sync --no-dev --frozen

# Copy source
COPY src/ src/

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "agent.api.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
