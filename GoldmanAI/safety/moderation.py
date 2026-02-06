"""Prompt moderation and policy decision helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ModerationResult:
    is_safe: bool
    reasons: list[str]


class SafetyModerator:
    """Loads static rules and evaluates prompt safety."""

    def __init__(self, rules_path: Path) -> None:
        self.rules_path = rules_path
        self.rules = self._load_rules(rules_path)

    @staticmethod
    def _load_rules(path: Path) -> dict[str, list[str]]:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)

    def evaluate(self, prompt: str, parental_education_mode: bool = True) -> ModerationResult:
        normalized = prompt.lower().strip()
        reasons: list[str] = []

        blocked_terms = self.rules.get("blocked_terms", [])
        restricted_visual_themes = self.rules.get("restricted_visual_themes", [])
        extra_terms = (
            self.rules.get("education_mode_extra_blocks", []) if parental_education_mode else []
        )

        for term in blocked_terms + restricted_visual_themes + extra_terms:
            if term in normalized:
                reasons.append(f"Blocked content detected: '{term}'")

        return ModerationResult(is_safe=not reasons, reasons=reasons)
