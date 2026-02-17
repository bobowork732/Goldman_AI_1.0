"""Mock video model with GPU-aware inference hooks."""

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

    def __init__(self, use_gpu: bool) -> None:
        self.use_gpu = use_gpu

    def infer_frames(
        self,
        params: VideoParams,
        source_image: str | None = None,
        multi_shot: bool = False,
        lip_sync_enabled: bool = False,
        lip_sync_focus: bool = False,
    ) -> list[str]:
        """Returns synthetic frame descriptors for demo purposes."""
        frame_count = params.fps * params.duration_seconds
        source = f" + animated from {source_image}" if source_image else ""
        lip_sync_tag = ""
        if lip_sync_enabled:
            lip_sync_tag = " | lip-sync=on"
            if lip_sync_focus:
                lip_sync_tag += "(focus)"

        if not multi_shot:
            return [
                f"frame_{idx:04d}: {params.style} {params.scene}, {params.lighting}, {params.motion}, {params.camera_type}{source}{lip_sync_tag}"
                for idx in range(frame_count)
            ]

        shots = ["wide establishing", "medium tracking", "close-up detail", "aerial sweep"]
        return [
            f"frame_{idx:04d}: shot={shots[idx % len(shots)]} | {params.style} {params.scene}, {params.lighting}, {params.motion}, {params.camera_type}{source}{lip_sync_tag}"
            for idx in range(frame_count)
        ]
