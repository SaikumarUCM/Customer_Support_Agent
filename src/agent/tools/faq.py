"""search_faq tool — looks up FAQ entries relevant to a customer query.

In a real deployment this would call a vector store (e.g. Pinecone, pgvector).
Here we use a small in-memory corpus so the project runs without external deps.
"""

from langchain_core.tools import tool

from agent.schemas.tools import FAQResult

_FAQ_CORPUS: list[dict[str, str]] = [
    {
        "question": "How do I track my order?",
        "answer": (
            "You can track your order by visiting your account page and clicking "
            "'Order History'. Each order has a tracking number linked to the carrier."
        ),
        "keywords": "track order tracking shipment delivery",
        "source": "help/shipping#tracking",
    },
    {
        "question": "How do I request a refund?",
        "answer": (
            "To request a refund, go to 'My Orders', select the order, and click "
            "'Request Refund'. Refunds are processed within 5–7 business days."
        ),
        "keywords": "refund money back return cancel payment",
        "source": "help/billing#refund",
    },
    {
        "question": "How do I reset my password?",
        "answer": (
            "Click 'Forgot Password' on the login page and enter your email address. "
            "You will receive a reset link valid for 30 minutes."
        ),
        "keywords": "password reset forgot login account",
        "source": "help/account#password",
    },
    {
        "question": "Can I change my subscription plan?",
        "answer": (
            "Yes. Go to 'Account > Subscription' and choose 'Change Plan'. "
            "Upgrades take effect immediately; downgrades apply at the next billing cycle."
        ),
        "keywords": "subscription plan upgrade downgrade billing change",
        "source": "help/billing#subscription",
    },
    {
        "question": "My product is damaged. What should I do?",
        "answer": (
            "We're sorry to hear that. Please take a photo of the damage and contact "
            "support within 48 hours of delivery. We will arrange a replacement or refund."
        ),
        "keywords": "damaged broken product defective replacement",
        "source": "help/returns#damaged",
    },
    {
        "question": "How long does shipping take?",
        "answer": (
            "Standard shipping takes 5–7 business days. Express shipping (2-day) and "
            "overnight options are available at checkout."
        ),
        "keywords": "shipping delivery time days express overnight",
        "source": "help/shipping#times",
    },
]


def _simple_score(query: str, entry: dict[str, str]) -> float:
    """Keyword-overlap scoring (placeholder for vector similarity)."""
    query_tokens = set(query.lower().split())
    doc_tokens = set(
        (entry["keywords"] + " " + entry["question"]).lower().split()
    )
    overlap = query_tokens & doc_tokens
    if not doc_tokens:
        return 0.0
    return round(len(overlap) / len(doc_tokens), 4)


@tool
def search_faq(query: str, top_k: int = 3) -> list[FAQResult]:
    """Search the FAQ knowledge base for entries relevant to the customer query.

    Args:
        query: The customer's query or extracted keywords.
        top_k: Maximum number of results to return (default 3).

    Returns:
        A list of FAQResult objects sorted by relevance score descending.
    """
    scored = [
        FAQResult(
            question=entry["question"],
            answer=entry["answer"],
            score=_simple_score(query, entry),
            source=entry["source"],
        )
        for entry in _FAQ_CORPUS
    ]
    scored.sort(key=lambda r: r.score, reverse=True)
    return scored[:top_k]
