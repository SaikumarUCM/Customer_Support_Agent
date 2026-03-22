"""Checkpointer factory.

Returns a MemorySaver by default.
If POSTGRES_DSN is set, upgrades to PostgresSaver for persistence across restarts.
"""

from langgraph.checkpoint.memory import MemorySaver

from agent.core.config import get_settings
from agent.core.logging import get_logger

log = get_logger(__name__)


def get_checkpointer() -> MemorySaver:
    """Return the appropriate LangGraph checkpointer.

    PostgresSaver is imported lazily so the project works without psycopg installed.
    """
    settings = get_settings()

    if settings.postgres_dsn:
        try:
            from langgraph.checkpoint.postgres import PostgresSaver  # type: ignore[import]

            log.info("Using PostgresSaver checkpointer", dsn=settings.postgres_dsn[:30] + "…")
            return PostgresSaver.from_conn_string(settings.postgres_dsn)
        except ImportError:
            log.warning(
                "POSTGRES_DSN is set but langgraph-checkpoint-postgres is not installed. "
                "Falling back to MemorySaver."
            )

    log.info("Using MemorySaver checkpointer (in-process, non-persistent)")
    return MemorySaver()
