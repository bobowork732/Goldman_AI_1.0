"""Bootstrap helpers for initializing directories and configs."""

from __future__ import annotations

from utils.config import AppConfig, DEFAULT_CONFIG


def prepare_environment(config: AppConfig | None = None) -> AppConfig:
    cfg = config or DEFAULT_CONFIG
    cfg.assets_output_dir.mkdir(parents=True, exist_ok=True)
    cfg.assets_temp_dir.mkdir(parents=True, exist_ok=True)
    cfg.logs_dir.mkdir(parents=True, exist_ok=True)
    cfg.safety_log_file.touch(exist_ok=True)
    return cfg
