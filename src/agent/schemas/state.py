"""AgentState — the single source of truth passed between graph nodes.

All nodes import from here; no node reaches into enriched.py or tools.py directly.
"""

from typing import Annotated, Any

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from agent.schemas.enriched import CustomerQuery
from agent.schemas.input import UserInput
from agent.schemas.tools import FAQResult, SupportTicket


def _last_wins(old: Any, new: Any) -> Any:  # noqa: ANN401
    """Reducer: new value always wins (used for scalar fields)."""
    return new


class AgentState(TypedDict):
    # ── Input ─────────────────────────────────────────────────────────────────
    user_input: Annotated[UserInput, _last_wins]

    # ── Enrichment ────────────────────────────────────────────────────────────
    customer_query: Annotated[CustomerQuery | None, _last_wins]

    # ── Tool outputs ──────────────────────────────────────────────────────────
    faq_results: Annotated[list[FAQResult], _last_wins]
    support_ticket: Annotated[SupportTicket | None, _last_wins]

    # ── Final response ────────────────────────────────────────────────────────
    response: Annotated[str, _last_wins]

    # ── LangGraph message history (used by compose_response node) ────────────
    messages: Annotated[list[Any], add_messages]

    # ── Run metadata ─────────────────────────────────────────────────────────
    run_id: Annotated[str, _last_wins]
    error: Annotated[str, _last_wins]


# Re-export schemas so nodes only need to import from state.py
__all__ = [
    "AgentState",
    "UserInput",
    "CustomerQuery",
    "FAQResult",
    "SupportTicket",
]
