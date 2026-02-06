"""Prompt safety filtering and sanitization."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from utils.helpers import now_iso
from utils.loader import load_json


@dataclass
class SafetyResult:
    allowed: bool
    sanitized_prompt: str
    blocked_terms: list[str]


class SafetyFilter:
    def __init__(self, rules_path: Path, log_path: Path) -> None:
        self.rules = load_json(rules_path)
        self.log_path = log_path

    def validate(self, prompt: str, parental_mode: bool = False) -> SafetyResult:
        blocked = []
        sanitized = prompt
        replacement = self.rules.get("safe_replacement", "safe cinematic scene")

        for term in self.rules.get("blocked_terms", []):
            if term.lower() in sanitized.lower():
                blocked.append(term)
                sanitized = self._case_insensitive_replace(sanitized, term, replacement)

        # stricter mode for children/education contexts.
        if parental_mode and "dark" in sanitized.lower():
            blocked.append("dark")
            sanitized = self._case_insensitive_replace(sanitized, "dark", "bright")

        allowed = True
        if blocked:
            self._log(prompt, sanitized, blocked, parental_mode)

        return SafetyResult(allowed=allowed, sanitized_prompt=sanitized, blocked_terms=blocked)

    def _log(self, original: str, sanitized: str, blocked: list[str], parental_mode: bool) -> None:
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as fh:
            fh.write(
                f"[{now_iso()}] parental_mode={parental_mode} blocked={blocked} | "
                f"original={original!r} | sanitized={sanitized!r}\n"
            )

    @staticmethod
    def _case_insensitive_replace(text: str, target: str, replacement: str) -> str:
        start = 0
        lower_text = text.lower()
        lower_target = target.lower()
        result = ""
        while True:
            idx = lower_text.find(lower_target, start)
            if idx == -1:
                result += text[start:]
                break
            result += text[start:idx] + replacement
            start = idx + len(target)
        return result
