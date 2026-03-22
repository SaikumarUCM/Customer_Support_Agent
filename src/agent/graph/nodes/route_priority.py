"""Conditional edge: decides whether to route to create_ticket or faq_lookup."""

from agent.graph.state import AgentState


def route_priority(state: AgentState) -> str:
    """Return the name of the next node based on priority.

    Returns:
        "create_ticket" if priority is "high", otherwise "faq_lookup".
    """
    customer_query = state.get("customer_query")
    if customer_query and customer_query.priority == "high":
        return "create_ticket"
    return "faq_lookup"
