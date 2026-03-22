"""Output guardrail — scrubs PII and checks tone before response reaches the caller."""

from agent.core.logging import get_logger
from agent.guardrails.rules import NEGATIVE_TONE_PHRASES, PII_PATTERNS

log = get_logger(__name__)


def scrub_pii(text: str) -> str:
    """Replace PII patterns in text with redaction placeholders."""
    for pattern, replacement in PII_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def check_tone(text: str) -> bool:
    """Return False if the response contains unacceptable tone phrases."""
    lower = text.lower()
    for phrase in NEGATIVE_TONE_PHRASES:
        if phrase in lower:
            log.warning("output_guard: negative tone detected", phrase=phrase)
            return False
    return True


def process_output(response: str) -> str:
    """Apply all output guardrails and return the cleaned response.

    Steps:
    1. Scrub PII.
    2. Tone check — replace with a safe fallback if tone is unacceptable.
    """
    cleaned = scrub_pii(response)

    if not check_tone(cleaned):
        log.warning("output_guard: replacing response due to tone violation")
        cleaned = (
            "I apologize for any inconvenience. Please contact our support team "
            "directly so we can assist you further."
        )

    return cleaned
