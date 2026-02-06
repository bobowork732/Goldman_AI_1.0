"""Stub audio model for synchronized voice/music generation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AudioParameters:
    duration: int
    language: str
    include_music: bool
    include_voice: bool


class AudioModel:
    def synthesize(self, transcript: str, params: AudioParameters) -> dict:
        return {
            "transcript": transcript,
            "duration": params.duration,
            "language": params.language,
            "music": params.include_music,
            "voice": params.include_voice,
        }
