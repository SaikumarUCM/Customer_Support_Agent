class AgentError(Exception):
    """Base error for all agent-related failures."""


class GuardrailError(AgentError):
    """Raised when input or output fails a guardrail check."""

    def __init__(self, message: str, rule: str = "") -> None:
        super().__init__(message)
        self.rule = rule


class ValidationError(AgentError):
    """Raised when structured output from the LLM fails Pydantic validation."""


class ToolError(AgentError):
    """Raised when a LangChain tool fails unexpectedly."""


class RateLimitError(AgentError):
    """Raised when the client exceeds the rate limit."""


class AuthenticationError(AgentError):
    """Raised when API key / Bearer token is missing or invalid."""
