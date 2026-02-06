"""Stub video model with GPU/CPU mode simulation."""

from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass
class VideoParameters:
    resolution: str
    fps: int
    duration: int
    motion_strength: float
    interpolation: bool


class VideoModel:
    def __init__(self) -> None:
        self.device = "gpu" if os.getenv("CUDA_VISIBLE_DEVICES") else "cpu"

    def infer(self, prompt: str, params: VideoParameters) -> dict:
        frame_count = params.fps * params.duration
        return {
            "device": self.device,
            "prompt": prompt,
            "frame_count": frame_count,
            "resolution": params.resolution,
            "interpolation": params.interpolation,
        }
