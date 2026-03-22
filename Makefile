.PHONY: install sync lint format typecheck test run docker-build docker-run clean

# ── uv setup ──────────────────────────────────────────────────────────────────
install:
	uv sync --all-extras

sync:
	uv sync

# ── Code quality ──────────────────────────────────────────────────────────────
lint:
	uv run ruff check src/ tests/

format:
	uv run ruff format src/ tests/
	uv run ruff check --fix src/ tests/

typecheck:
	uv run mypy src/

# ── Tests ─────────────────────────────────────────────────────────────────────
test:
	uv run pytest tests/ -v --cov=src/agent --cov-report=term-missing

test-fast:
	uv run pytest tests/ -v -x -q

# ── Run ───────────────────────────────────────────────────────────────────────
run:
	uv run uvicorn src.agent.api.app:create_app --factory --host 0.0.0.0 --port 8000 --reload

run-prod:
	uv run uvicorn src.agent.api.app:create_app --factory --host 0.0.0.0 --port 8000 --workers 4

# ── Docker ────────────────────────────────────────────────────────────────────
docker-build:
	docker build -t customer-support-agent:latest .

docker-run:
	docker run --env-file .env -p 8000:8000 customer-support-agent:latest

# ── Cleanup ───────────────────────────────────────────────────────────────────
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -name "*.pyc" -delete
