"""Node: faq_lookup — calls the search_faq tool and stores results in state."""

from agent.core.logging import get_logger
from agent.graph.state import AgentState
from agent.tools.faq import search_faq

log = get_logger(__name__)


async def faq_lookup_node(state: AgentState) -> dict:
    """Search the FAQ knowledge base using extracted keywords."""
    customer_query = state["customer_query"]
    user_input = state["user_input"]

    # Build a search string from keywords + original message
    keywords_str = " ".join(customer_query.keywords) if customer_query.keywords else ""
    search_query = f"{keywords_str} {user_input.message}".strip()

    log.info("faq_lookup: searching", query=search_query[:80])
    results = search_faq.invoke({"query": search_query, "top_k": 3})
    log.info("faq_lookup: done", result_count=len(results))

    return {"faq_results": results}
