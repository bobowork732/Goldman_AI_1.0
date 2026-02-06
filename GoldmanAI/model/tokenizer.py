"""Prompt understanding engine for extracting generation controls."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ParsedPrompt:
    scene: str
    lighting: str
    motion: str
    style: str
    camera_type: str


class PromptTokenizer:
    """Very lightweight rule-based parser for structured prompt fields."""

    _LIGHTING = ("golden hour", "cinematic", "night", "neon", "studio", "sunset", "soft")
    _MOTION = ("slow pan", "fast", "drone", "orbit", "timelapse", "stabilized")
    _STYLE = ("realistic", "anime", "watercolor", "3d", "documentary", "retro")
    _CAMERA = ("wide", "close-up", "macro", "aerial", "tracking", "handheld")

    def parse(self, prompt: str) -> ParsedPrompt:
        lower = prompt.lower()
        return ParsedPrompt(
            scene=self._extract_scene(prompt),
            lighting=self._find_first(lower, self._LIGHTING, default="natural"),
            motion=self._find_first(lower, self._MOTION, default="gentle"),
            style=self._find_first(lower, self._STYLE, default="realistic"),
            camera_type=self._find_first(lower, self._CAMERA, default="wide"),
        )

    @staticmethod
    def _find_first(text: str, items: tuple[str, ...], default: str) -> str:
        for item in items:
            if item in text:
                return item
        return default

    @staticmethod
    def _extract_scene(prompt: str) -> str:
        if " in " in prompt:
            return prompt.split(" in ", maxsplit=1)[-1][:120].strip()
        return prompt[:120].strip()
