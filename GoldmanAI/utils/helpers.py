"""Utility functions used across the app."""

from __future__ import annotations

from datetime import datetime


def timestamp_slug() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")
