"""Heuristics for filtering low-value memory notes."""

from __future__ import annotations

import re

# Visual fluff, meta replies, or throwaway chat — not durable memories.
_REJECT_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\b(smily|smiley|emoji|emoticon|emote)\b",
        r"\b(hand next to|next to (?:its|his|her) mouth)\b",
        r"\b(facial expression|body language|gesture|pose|sprite|avatar)\b",
        r"\b(describ(es|ing|ed)|depict(s|ing|ed)|shows?|showing)\b.*\b(face|look|expression|mouth|hand|emoji|smiley)\b",
        r"^(no change needed|nothing to store|none|n/?a)\.?$",
        r"^[\W\d_]+$",
        r"^(thanks|thank you|thx|ok|okay|sure|yes|no|hi|hello|hey|cool|nice|great)\.?$",
        r"\buser (just )?said (hi|hello|hey|thanks)\b",
        r"\b(had a|having a) (good|great|nice|lovely|fine) (day|morning|evening)\b",
        r"\b(the weather is|nice weather|beautiful day)\b",
    )
)

# Durable user info, preferences, plans, people, or meaningful Kinito observations.
_MEMORY_HINTS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\b(user|i am|i'm|i like|i love|i enjoy|i work|i study|i live|my )\b",
        r"\b(works?|working as|studies|student|employed)\b",
        r"\b(likes?|loves?|enjoys?|prefers?|dislikes?|favorite|wants? to)\b",
        r"\b(plan|plans|friend|family|partner|pet|job|hobby|weekend|birthday)\b",
        r"\b(with [A-Z][a-z]+|named [A-Z])",
        r"\b(movie night|game night|appointment|meeting|trip|vacation)\b",
        r"^[a-z_]+:\s+\S",
        r"\b(has a|have a|owns a|got a)\b",
        r"\b(hiking|often|usually|every|tends? to|seems to)\b",
        r"\b(noticed (that )?user|observed (that )?user|user (often|usually|mentioned))\b",
        r"\b(speaks?|language|german|english|deutsch)\b",
    )
)

_MIN_NOTE_LEN = 10


def is_storable_note(text: str, *, source: str = "chat") -> bool:
    """Return True if a note is worth persisting."""
    trimmed = text.strip()
    if not trimmed:
        return False

    if source == "question":
        return True

    lower = trimmed.lower()
    for pattern in _REJECT_PATTERNS:
        if pattern.search(lower):
            return False

    if len(trimmed) < _MIN_NOTE_LEN:
        return False

    return any(pattern.search(trimmed) for pattern in _MEMORY_HINTS)
