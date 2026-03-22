from typing import Literal

from pydantic import BaseModel, Field


class CustomerQuery(BaseModel):
    """Enriched, LLM-structured representation of a customer query.

    The enrichment chain populates this from a raw UserInput.
    All fields are required — the LLM must provide them all.
    """

    intent: str = Field(
        ...,
        description=(
            "One-line summary of what the customer wants, e.g. "
            "'track missing order', 'request refund', 'cancel subscription'"
        ),
    )
    category: Literal[
        "billing",
        "shipping",
        "technical",
        "account",
        "product",
        "other",
    ] = Field(..., description="Top-level support category")
    priority: Literal["low", "medium", "high"] = Field(
        ...,
        description=(
            "Urgency level. Use 'high' when the customer is frustrated, "
            "reports financial loss, or needs immediate resolution."
        ),
    )
    sentiment: Literal["positive", "neutral", "negative"] = Field(
        ..., description="Overall emotional tone of the message"
    )
    keywords: list[str] = Field(
        default_factory=list,
        description="3-7 keywords extracted from the message useful for FAQ search",
    )
    language: str = Field(
        default="en",
        description="Detected BCP-47 language tag",
    )
    requires_human: bool = Field(
        default=False,
        description="True if the query cannot be resolved by AI alone",
    )
