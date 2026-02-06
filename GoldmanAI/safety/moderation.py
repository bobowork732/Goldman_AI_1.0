"""Higher-level moderation checks."""

from __future__ import annotations

from dataclasses import dataclass

from safety.filter import SafetyFilter, SafetyResult


@dataclass
class ModerationDecision:
    approved: bool
    reason: str
    result: SafetyResult


class Moderator:
    def __init__(self, safety_filter: SafetyFilter) -> None:
        self.safety_filter = safety_filter

    def moderate_prompt(self, prompt: str, parental_mode: bool = False) -> ModerationDecision:
        result = self.safety_filter.validate(prompt, parental_mode=parental_mode)
        if result.blocked_terms:
            return ModerationDecision(
                approved=True,
                reason="Prompt sanitized to safe version",
                result=result,
            )
        return ModerationDecision(approved=True, reason="Prompt approved", result=result)
