"""Response chain: assembles the final plain-English reply for the customer."""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from agent.core.config import get_settings
from agent.schemas.enriched import CustomerQuery
from agent.schemas.tools import FAQResult, SupportTicket

_PROMPT_DIR = Path(__file__).parent / "prompts"
_jinja_env = Environment(loader=FileSystemLoader(str(_PROMPT_DIR)), autoescape=False)


def _render_response_prompt(
    message: str,
    query: CustomerQuery,
    faq_results: list[FAQResult],
    ticket: SupportTicket | None,
) -> str:
    template = _jinja_env.get_template("compose_response.j2")
    return template.render(
        message=message,
        intent=query.intent,
        category=query.category,
        priority=query.priority,
        sentiment=query.sentiment,
        faq_results=faq_results,
        ticket=ticket,
    )


def build_response_chain() -> ChatOpenAI:
    settings = get_settings()
    return ChatOpenAI(
        model=settings.model_name,
        temperature=0.4,  # slightly more creative for human-facing text
        api_key=settings.openai_api_key,
    )


_response_llm: ChatOpenAI | None = None


def get_response_llm() -> ChatOpenAI:
    global _response_llm
    if _response_llm is None:
        _response_llm = build_response_chain()
    return _response_llm


async def compose_response(
    message: str,
    query: CustomerQuery,
    faq_results: list[FAQResult],
    ticket: SupportTicket | None,
) -> str:
    """Compose a customer-facing response string."""
    llm = get_response_llm()
    rendered = _render_response_prompt(message, query, faq_results, ticket)
    result = await llm.ainvoke([HumanMessage(content=rendered)])
    return result.content  # type: ignore[return-value]
