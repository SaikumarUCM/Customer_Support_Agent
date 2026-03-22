"""Input guardrail — blocks prompt injection, abuse, and obvious PII leakage."""

from agent.core.exceptions import GuardrailError
from agent.core.logging import get_logger
from agent.guardrails.rules import ABUSE_KEYWORDS, INJECTION_PATTERNS
from agent.schemas.input import UserInput

log = get_logger(__name__)


def check_input(user_input: UserInput) -> None:
    """Raise GuardrailError if the input violates any safety rule.

    Args:
        user_input: The validated UserInput from the API layer.

    Raises:
        GuardrailError: with `.rule` set to the name of the triggered rule.
    """
    message = user_input.message

    # 1. Prompt injection
    for pattern in INJECTION_PATTERNS:
        if pattern.search(message):
            log.warning(
                "input_guard: injection attempt blocked",
                user_id=user_input.user_id,
                pattern=pattern.pattern,
            )
            raise GuardrailError(
                "Your message contains content that cannot be processed.",
                rule="prompt_injection",
            )

    # 2. Abusive content
    lower = message.lower()
    for keyword in ABUSE_KEYWORDS:
        if keyword in lower:
            log.warning(
                "input_guard: abusive content blocked",
                user_id=user_input.user_id,
                keyword=keyword,
            )
            raise GuardrailError(
                "Your message contains inappropriate content.",
                rule="abuse",
            )

    # 3. Excessive length (double-check beyond Pydantic's max_length)
    if len(message) > 4000:
        raise GuardrailError("Message is too long.", rule="length_limit")
