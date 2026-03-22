"""Enrichment chain: UserInput → CustomerQuery via structured output."""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from agent.core.config import get_settings
from agent.schemas.enriched import CustomerQuery
from agent.schemas.input import UserInput

_PROMPT_DIR = Path(__file__).parent / "prompts"
_jinja_env = Environment(loader=FileSystemLoader(str(_PROMPT_DIR)), autoescape=False)


def _render_enrich_prompt(user_input: UserInput) -> str:
    template = _jinja_env.get_template("enrich_query.j2")
    return template.render(message=user_input.message)


def build_enrichment_chain() -> object:
    """Return a runnable chain: UserInput → CustomerQuery."""
    settings = get_settings()

    llm = ChatOpenAI(
        model=settings.model_name,
        temperature=settings.model_temperature,
        api_key=settings.openai_api_key,
    )

    structured_llm = llm.with_structured_output(CustomerQuery)

    prompt = ChatPromptTemplate.from_messages(
        [("human", "{rendered_prompt}")]
    )

    chain = prompt | structured_llm
    return chain


# Singleton — built once per process
_enrichment_chain = None


def get_enrichment_chain() -> object:
    global _enrichment_chain
    if _enrichment_chain is None:
        _enrichment_chain = build_enrichment_chain()
    return _enrichment_chain


async def enrich_user_input(user_input: UserInput) -> CustomerQuery:
    """Run the enrichment chain and return a validated CustomerQuery."""
    chain = get_enrichment_chain()
    rendered = _render_enrich_prompt(user_input)
    result: CustomerQuery = await chain.ainvoke({"rendered_prompt": rendered})
    return result
