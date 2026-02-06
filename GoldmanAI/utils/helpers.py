"""Helper utilities used by generation modules."""

from __future__ import annotations

from datetime import datetime


def now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(max_value, value))
