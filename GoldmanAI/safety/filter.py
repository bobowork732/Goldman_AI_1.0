"""Safety filter wrapper for protected generation calls."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Any

from .moderation import SafetyModerator


class SafeGenerationError(RuntimeError):
    """Raised when a prompt is rejected by the safety layer."""


class SafetyFilter:
    """Validates prompts and logs blocked requests."""

    def __init__(self, moderator: SafetyModerator, safety_log_path: Path) -> None:
        self.moderator = moderator
        self.safety_log_path = safety_log_path
        self.safety_log_path.parent.mkdir(parents=True, exist_ok=True)
        self.safety_log_path.touch(exist_ok=True)

    def validate_prompt(self, prompt: str, parental_education_mode: bool = True) -> tuple[bool, list[str]]:
        moderation = self.moderator.evaluate(prompt, parental_education_mode=parental_education_mode)
        if not moderation.is_safe:
            self._log_filtered_prompt(prompt, moderation.reasons)
        return moderation.is_safe, moderation.reasons

    def safe_generate(
        self,
        prompt: str,
        generator: Callable[..., Any],
        *args: Any,
        parental_education_mode: bool = True,
        **kwargs: Any,
    ) -> Any:
        """Guarded wrapper for generation calls."""
        is_safe, reasons = self.validate_prompt(prompt, parental_education_mode=parental_education_mode)
        if not is_safe:
            raise SafeGenerationError("; ".join(reasons))
        return generator(prompt, *args, **kwargs)

    def _log_filtered_prompt(self, prompt: str, reasons: list[str]) -> None:
        ts = datetime.now(tz=timezone.utc).isoformat()
        reason_text = " | ".join(reasons)
        with self.safety_log_path.open("a", encoding="utf-8") as fh:
            fh.write(f"[{ts}] BLOCKED PROMPT: {prompt} :: {reason_text}\n")
