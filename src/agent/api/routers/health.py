"""Health and readiness probes."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: str


@router.get("/health", response_model=HealthResponse, summary="Liveness probe")
async def health() -> HealthResponse:
    """Always returns 200 if the process is alive."""
    return HealthResponse(status="ok")


@router.get("/ready", response_model=HealthResponse, summary="Readiness probe")
async def ready() -> HealthResponse:
    """Returns 200 when the graph and chains are loaded and ready."""
    from agent.graph.builder import get_graph  # noqa: PLC0415

    get_graph()  # will raise if graph is broken
    return HealthResponse(status="ready")
