"""Central configuration values for Goldman AI."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class SafetyConfig:
    """Safety-related toggles and limits."""

    enabled: bool = True
    parental_education_mode: bool = True
    strict_blocking: bool = True


@dataclass(slots=True)
class RenderConfig:
    """Rendering defaults used by the generation pipeline."""

    resolution: tuple[int, int] = (1280, 720)
    fps: int = 24
    duration_seconds: int = 5
    motion_strength: float = 0.6
    frame_interpolation: bool = True
    render_speed: str = "balanced"


@dataclass(slots=True)
class AppConfig:
    """Top-level application config object."""

    project_root: Path = field(default_factory=lambda: Path(__file__).resolve().parents[1])
    assets_output_dir: Path = field(init=False)
    assets_temp_dir: Path = field(init=False)
    logs_dir: Path = field(init=False)
    safety_log_file: Path = field(init=False)
    safety: SafetyConfig = field(default_factory=SafetyConfig)
    render: RenderConfig = field(default_factory=RenderConfig)

    def __post_init__(self) -> None:
        self.assets_output_dir = self.project_root / "assets" / "output"
        self.assets_temp_dir = self.project_root / "assets" / "temp"
        self.logs_dir = self.project_root / "logs"
        self.safety_log_file = self.logs_dir / "safety_log.txt"


DEFAULT_CONFIG = AppConfig()
