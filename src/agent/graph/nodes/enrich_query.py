"""Node: enrich_query — converts UserInput → CustomerQuery via structured LLM output."""

from agent.chains.enrichment_chain import enrich_user_input
from agent.core.logging import get_logger
from agent.graph.state import AgentState

log = get_logger(__name__)


async def enrich_query_node(state: AgentState) -> dict:
    """LLM call: UserInput → CustomerQuery (Pydantic-validated)."""
    user_input = state["user_input"]
    log.info("enrich_query: start", user_id=user_input.user_id)

    customer_query = await enrich_user_input(user_input)

    log.info(
        "enrich_query: done",
        intent=customer_query.intent,
        priority=customer_query.priority,
        category=customer_query.category,
    )
    return {"customer_query": customer_query}
