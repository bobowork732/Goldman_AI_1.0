"""Renderer utilities writing placeholder outputs."""

from __future__ import annotations

from pathlib import Path


class Renderer:
    def render_mp4(self, output_path: Path, metadata: dict) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        # Placeholder MP4 artifact (metadata text); replace with real encoder later.
        output_path.write_text(f"FAKE_MP4\n{metadata}\n", encoding="utf-8")
        return output_path

    def render_wav(self, output_path: Path, metadata: dict) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(f"FAKE_WAV\n{metadata}\n", encoding="utf-8")
        return output_path
