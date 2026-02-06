"""UI control models and default values."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class UISettings:
    safety_mode: bool = True
    resolution: str = "1280x720"
    render_speed: str = "balanced"
