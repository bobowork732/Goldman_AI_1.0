"""Prompt tokenizer and parser."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PromptFeatures:
    scene: str
    lighting: str
    motion: str
    style: str
    camera_type: str


class PromptTokenizer:
    def parse(self, prompt: str) -> PromptFeatures:
        lower = prompt.lower()
        lighting = "cinematic" if "cinematic" in lower else "natural"
        style = "photoreal" if "realistic" in lower or "cinematic" in lower else "stylized"
        motion = "smooth" if "slow" in lower or "walking" in lower else "standard"
        camera_type = "dolly" if "dolly" in lower else "stabilized"
        scene = prompt.strip() or "safe cinematic environment"
        return PromptFeatures(scene=scene, lighting=lighting, motion=motion, style=style, camera_type=camera_type)
