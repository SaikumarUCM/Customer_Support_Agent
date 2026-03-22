"""Node: create_ticket — creates a support ticket for high-priority queries."""

from agent.core.logging import get_logger
from agent.graph.state import AgentState
from agent.tools.ticketing import create_support_ticket

log = get_logger(__name__)


async def create_ticket_node(state: AgentState) -> dict:
    """Create a support ticket and store it in state."""
    customer_query = state["customer_query"]
    user_input = state["user_input"]

    log.info(
        "create_ticket: creating",
        user_id=user_input.user_id,
        priority=customer_query.priority,
    )

    ticket = create_support_ticket.invoke(
        {
            "user_id": user_input.user_id,
            "summary": customer_query.intent,
            "priority": customer_query.priority,
            "category": customer_query.category,
        }
    )

    log.info("create_ticket: done", ticket_id=ticket.ticket_id)
    return {"support_ticket": ticket}
