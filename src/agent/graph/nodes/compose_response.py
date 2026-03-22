"""Node: compose_response — generates the final customer-facing reply."""

from agent.chains.response_chain import compose_response
from agent.core.logging import get_logger
from agent.graph.state import AgentState

log = get_logger(__name__)


async def compose_response_node(state: AgentState) -> dict:
    """Final LLM call: build a plain-English response from all accumulated context."""
    user_input = state["user_input"]
    customer_query = state["customer_query"]
    faq_results = state.get("faq_results", [])
    ticket = state.get("support_ticket")

    log.info(
        "compose_response: start",
        has_faq=bool(faq_results),
        has_ticket=bool(ticket),
    )

    response_text = await compose_response(
        message=user_input.message,
        query=customer_query,
        faq_results=faq_results,
        ticket=ticket,
    )

    log.info("compose_response: done", response_length=len(response_text))
    return {"response": response_text}
