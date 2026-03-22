"""create_support_ticket tool — creates a support ticket for high-priority queries.

In a real deployment this would call a ticketing system (e.g. Zendesk, Jira).
Here we generate a deterministic stub ticket so the project runs offline.
"""

import hashlib
import uuid
from datetime import UTC, datetime

from langchain_core.tools import tool

from agent.schemas.tools import SupportTicket


@tool
def create_support_ticket(
    user_id: str,
    summary: str,
    priority: str,
    category: str,
) -> SupportTicket:
    """Create a support ticket for a customer issue that requires human attention.

    Args:
        user_id: Unique identifier of the customer.
        summary: One-line description of the issue.
        priority: Ticket priority — 'low', 'medium', or 'high'.
        category: Support category — e.g. 'billing', 'shipping', 'technical'.

    Returns:
        A SupportTicket with a unique ticket_id and creation timestamp.
    """
    # Deterministic but unique ticket ID based on user + summary + time
    raw = f"{user_id}:{summary}:{datetime.now(UTC).isoformat()}"
    short_hash = hashlib.md5(raw.encode()).hexdigest()[:8]  # noqa: S324
    ticket_id = f"TICKET-{datetime.now(UTC).strftime('%Y%m%d')}-{short_hash}"

    return SupportTicket(
        ticket_id=ticket_id,
        status="open",
        priority=priority,
        category=category,
        summary=summary,
        created_at=datetime.now(UTC).isoformat(),
        assigned_to="",  # will be assigned by the ticketing system
    )
