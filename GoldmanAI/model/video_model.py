"""Mock video generation model (version 1) with GPU-aware inference hooks."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class VideoParams:
    scene: str
    lighting: str
    motion: str
    style: str
    camera_type: str
    fps: int
    duration_seconds: int
    motion_strength: float


class VideoModel:
    """Represents the text/image-to-video model facade."""

    VERSION = "1.0"

    def __init__(self, use_gpu: bool) -> None:
        self.use_gpu = use_gpu

    def infer_frames(self, params: VideoParams, source_image: str | None = None) -> list[str]:
        """Returns synthetic frame descriptors for demo purposes."""
        # Bugfix: avoid generating an empty timeline when bad runtime values are provided.
        frame_count = max(1, params.fps * params.duration_seconds)
        source = f" + animated from {source_image}" if source_image else ""
        motion_weight = max(0.0, min(1.0, params.motion_strength))
        engine = "gpu" if self.use_gpu else "cpu"
        return [
            (
                f"v{self.VERSION} frame_{idx:04d}: {params.style} {params.scene}, "
                f"{params.lighting}, {params.motion}, {params.camera_type}, "
                f"motion_strength={motion_weight:.2f}, backend={engine}{source}"
            )
            for idx in range(frame_count)
        ]
