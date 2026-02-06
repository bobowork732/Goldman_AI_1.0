"""Configuration defaults for Goldman AI."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass
class AppConfig:
    project_name: str = "Goldman AI"
    version: str = "1.0"
    default_resolution: str = "1920x1080"
    default_fps: int = 24
    default_duration: int = 5
    default_motion_strength: float = 0.6
    parental_mode_default: bool = False
    output_dir: Path = BASE_DIR / "assets" / "output"
    temp_dir: Path = BASE_DIR / "assets" / "temp"
    safety_rules: Path = BASE_DIR / "safety" / "rules.json"
    safety_log: Path = BASE_DIR / "logs" / "safety_log.txt"


CONFIG = AppConfig()
