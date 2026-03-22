"""POST /chat — the main endpoint that runs the LangGraph agent."""

import uuid

from fastapi import APIRouter, HTTPException, Request, status
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel

from agent.core.exceptions import GuardrailError
from agent.core.logging import get_logger
from agent.graph.builder import get_graph
from agent.guardrails.input_guard import check_input
from agent.guardrails.output_guard import process_output
from agent.observability.tracing import trace_run
from agent.schemas.input import UserInput

log = get_logger(__name__)
router = APIRouter(tags=["chat"])


class ChatResponse(BaseModel):
    response: str
    priority: str
    ticket_id: str | None = None
    run_id: str
    session_id: str


@router.post("/chat", response_model=ChatResponse, summary="Submit a support query")
async def chat(request: Request, body: UserInput) -> ChatResponse:
    """Process a customer support message through the full LangGraph pipeline.

    Flow:
    1. input_guard  → block injection / abuse
    2. LangGraph    → enrich → route → (faq_lookup | create_ticket) → compose_response
    3. output_guard → scrub PII, tone check
    """
    run_id = str(uuid.uuid4())

    # ── 1. Input guardrail ────────────────────────────────────────────────────
    try:
        check_input(body)
    except GuardrailError as exc:
        log.warning("chat: input blocked", rule=exc.rule, user_id=body.user_id)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    # ── 2. Run LangGraph ──────────────────────────────────────────────────────
    graph = get_graph()
    thread_id = body.session_id or run_id

    initial_state = {
        "user_input": body,
        "customer_query": None,
        "faq_results": [],
        "support_ticket": None,
        "response": "",
        "messages": [],
        "run_id": run_id,
        "error": "",
    }

    config: RunnableConfig = {
        "configurable": {"thread_id": thread_id},
        "run_id": uuid.UUID(run_id),
        "tags": ["customer-support", f"user:{body.user_id}"],
    }

    log.info("chat: invoking graph", run_id=run_id, user_id=body.user_id)

    try:
        with trace_run(run_id=run_id, user_id=body.user_id):
            final_state = await graph.ainvoke(initial_state, config=config)
    except Exception as exc:
        log.error("chat: graph error", run_id=run_id, error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request.",
        ) from exc

    # ── 3. Output guardrail ───────────────────────────────────────────────────
    raw_response: str = final_state.get("response", "")
    safe_response = process_output(raw_response)

    ticket = final_state.get("support_ticket")
    customer_query = final_state.get("customer_query")

    return ChatResponse(
        response=safe_response,
        priority=customer_query.priority if customer_query else "medium",
        ticket_id=ticket.ticket_id if ticket else None,
        run_id=run_id,
        session_id=thread_id,
    )
