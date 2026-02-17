"""Renderer module: handles interpolation and MP4 export placeholder."""

from __future__ import annotations

from pathlib import Path


class Renderer:
    """Frame post-processing and file emission."""

    def interpolate_frames(self, frames: list[str], enabled: bool) -> list[str]:
        if not enabled:
            return frames
        interpolated: list[str] = []
        for frame in frames:
            interpolated.append(frame)
            interpolated.append(f"{frame} [interpolated]")
        return interpolated

    def export_mp4(self, frames: list[str], output_path: Path, fps: int) -> Path:
        """Writes a lightweight pseudo-MP4 text payload to keep example dependency-free."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as fh:
            fh.write(f"Pseudo MP4 export (fps={fps})\n")
            fh.write("\n".join(frames))
        return output_path

    def export_mix_manifest(self, video_path: Path, audio_path: Path | None, output_path: Path) -> Path:
        """Writes a simple mix descriptor representing synchronized video+audio packaging."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as fh:
            fh.write("Goldman AI Mix Package\n")
            fh.write(f"video={video_path.name}\n")
            fh.write(f"audio={audio_path.name if audio_path else 'off'}\n")
        return output_path
