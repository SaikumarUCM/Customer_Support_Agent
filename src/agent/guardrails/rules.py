"""Shared regex / keyword rule lists for input and output guardrails."""

import re

# ── Prompt injection patterns ─────────────────────────────────────────────────
INJECTION_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"ignore (all |previous |above )?(instructions?|prompts?|rules?)", re.I),
    re.compile(r"disregard (all |previous |above )?(instructions?|prompts?|rules?)", re.I),
    re.compile(r"you are now", re.I),
    re.compile(r"act as (a |an |the )?(?!support)", re.I),
    re.compile(r"pretend (you are|to be)", re.I),
    re.compile(r"jailbreak", re.I),
    re.compile(r"DAN mode", re.I),
    re.compile(r"developer mode", re.I),
    re.compile(r"system prompt", re.I),
    re.compile(r"<\s*script", re.I),
]

# ── Abusive / toxic content keywords ─────────────────────────────────────────
ABUSE_KEYWORDS: list[str] = [
    "kill yourself",
    "go die",
    "i will hurt",
    "i will kill",
    "bomb threat",
]

# ── PII patterns (for output scrubbing) ──────────────────────────────────────
PII_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    # Credit card numbers (simplified)
    (re.compile(r"\b(?:\d[ -]?){13,16}\b"), "[CARD REDACTED]"),
    # Social security numbers
    (re.compile(r"\b\d{3}[-–]\d{2}[-–]\d{4}\b"), "[SSN REDACTED]"),
    # Email addresses
    (re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"), "[EMAIL REDACTED]"),
    # Phone numbers (North-American style)
    (re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b"), "[PHONE REDACTED]"),
]

# ── Minimum response tone check ───────────────────────────────────────────────
NEGATIVE_TONE_PHRASES: list[str] = [
    "i don't care",
    "not my problem",
    "deal with it",
    "figure it out yourself",
    "too bad",
]
