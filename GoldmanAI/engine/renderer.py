"""Renderer module: handles frame processing and pseudo MP4 export."""

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

    def apply_blur_then_sharpen(self, frames: list[str]) -> list[str]:
        """Apply ordered post-processing markers: blur -> sharpen -> result."""
        post_processed: list[str] = []
        for frame in frames:
            blurred = f"{frame} [blur]"
            sharpened = f"{blurred} [sharp]"
            result = f"{sharpened} [result]"
            post_processed.append(result)
        return post_processed

    def export_mp4(self, frames: list[str], output_path: Path, fps: int) -> Path:
        """Writes a lightweight pseudo-MP4 text payload to keep example dependency-free."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as fh:
            fh.write(f"Pseudo MP4 export (fps={fps})\n")
            fh.write("\n".join(frames))
        return output_path

    def mux_audio_video(self, video_path: Path, audio_path: Path, output_path: Path) -> Path:
        """Create a pseudo muxed video+audio artifact."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as fh:
            fh.write("Pseudo MP4 with audio\n")
            fh.write(f"video_source={video_path}\n")
            fh.write(f"audio_source={audio_path}\n")
        return output_path
