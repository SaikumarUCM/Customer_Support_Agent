"""Assemble the LangGraph StateGraph.

Graph topology
──────────────
START
  └─▶ enrich_query
        └─▶ route_priority  (conditional edge)
              ├─▶ create_ticket  ──▶ compose_response ──▶ END
              └─▶ faq_lookup     ──▶ compose_response ──▶ END
"""

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from agent.graph.checkpointer import get_checkpointer
from agent.graph.nodes import (
    compose_response_node,
    create_ticket_node,
    enrich_query_node,
    faq_lookup_node,
    route_priority,
)
from agent.graph.state import AgentState


def build_graph() -> CompiledStateGraph:
    """Build and compile the customer support StateGraph."""
    graph = StateGraph(AgentState)

    # ── Nodes ─────────────────────────────────────────────────────────────────
    graph.add_node("enrich_query", enrich_query_node)
    graph.add_node("faq_lookup", faq_lookup_node)
    graph.add_node("create_ticket", create_ticket_node)
    graph.add_node("compose_response", compose_response_node)

    # ── Edges ─────────────────────────────────────────────────────────────────
    graph.add_edge(START, "enrich_query")

    graph.add_conditional_edges(
        "enrich_query",
        route_priority,
        {
            "faq_lookup": "faq_lookup",
            "create_ticket": "create_ticket",
        },
    )

    graph.add_edge("faq_lookup", "compose_response")
    graph.add_edge("create_ticket", "compose_response")
    graph.add_edge("compose_response", END)

    checkpointer = get_checkpointer()
    return graph.compile(checkpointer=checkpointer)


# Singleton compiled graph
_graph = None


def get_graph() -> CompiledStateGraph:
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph
