from pydantic import BaseModel, Field


class FAQResult(BaseModel):
    """A single FAQ entry returned by the search_faq tool."""

    question: str = Field(..., description="The FAQ question")
    answer: str = Field(..., description="The FAQ answer")
    score: float = Field(..., ge=0.0, le=1.0, description="Relevance score (0–1)")
    source: str = Field(default="", description="Source document or URL")


class SupportTicket(BaseModel):
    """A support ticket created by the create_support_ticket tool."""

    ticket_id: str = Field(..., description="Unique ticket identifier")
    status: str = Field(default="open", description="Current ticket status")
    priority: str = Field(..., description="Ticket priority: low | medium | high")
    category: str = Field(..., description="Support category")
    summary: str = Field(..., description="One-line summary of the issue")
    created_at: str = Field(..., description="ISO-8601 creation timestamp")
    assigned_to: str = Field(default="", description="Agent assigned to this ticket")
