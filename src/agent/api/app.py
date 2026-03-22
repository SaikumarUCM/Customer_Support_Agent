"""FastAPI application factory with lifespan management."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from agent.api.middleware.auth import AuthMiddleware
from agent.api.routers import chat_router, health_router
from agent.observability.feedback import router as feedback_router
from agent.core.config import get_settings
from agent.core.logging import configure_logging, get_logger

log = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup and shutdown lifecycle."""
    settings = get_settings()
    configure_logging(settings.log_level)

    # Configure LangSmith tracing env vars before anything imports langchain
    if settings.tracing_enabled:
        import os  # noqa: PLC0415

        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = settings.langchain_api_key
        os.environ["LANGCHAIN_PROJECT"] = settings.langchain_project
        os.environ["LANGCHAIN_ENDPOINT"] = settings.langchain_endpoint

    # Eagerly build the graph so the first request isn't slow
    from agent.graph.builder import get_graph  # noqa: PLC0415

    get_graph()

    log.info(
        "agent started",
        env=settings.app_env,
        model=settings.model_name,
        tracing=settings.tracing_enabled,
    )

    yield

    log.info("agent shutting down")


def create_app() -> FastAPI:
    """Application factory — called by uvicorn --factory."""
    settings = get_settings()

    app = FastAPI(
        title="Customer Support Agent",
        description="AI-powered support agent powered by LangGraph + LangChain.",
        version="0.1.0",
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        lifespan=lifespan,
    )

    # ── Auth middleware ────────────────────────────────────────────────────────
    app.add_middleware(AuthMiddleware)

    # ── Routers ───────────────────────────────────────────────────────────────
    app.include_router(health_router)
    app.include_router(chat_router)
    app.include_router(feedback_router)

    return app
