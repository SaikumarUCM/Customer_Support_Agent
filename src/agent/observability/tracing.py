"""LangSmith tracing helpers."""

from contextlib import contextmanager
from typing import Generator

from agent.core.config import get_settings
from agent.core.logging import get_logger

log = get_logger(__name__)


@contextmanager
def trace_run(run_id: str, user_id: str) -> Generator[None, None, None]:
    """Context manager that attaches run metadata for LangSmith tracing.

    When tracing is disabled this is a no-op, so the graph code path is identical.
    """
    settings = get_settings()

    if not settings.tracing_enabled:
        yield
        return

    try:
        from langsmith import trace  # type: ignore[import]  # noqa: PLC0415

        metadata = {"run_id": run_id, "user_id": user_id}
        with trace(
            name="customer_support_agent",
            run_type="chain",
            project_name=settings.langchain_project,
            metadata=metadata,
        ):
            yield
    except ImportError:
        log.warning("langsmith not installed — tracing disabled")
        yield
    except Exception as exc:
        log.warning("tracing error (non-fatal)", error=str(exc))
        yield
