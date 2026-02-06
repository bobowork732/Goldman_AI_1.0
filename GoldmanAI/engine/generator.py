"""Generation orchestrator for video+audio inference."""

from __future__ import annotations

from pathlib import Path

from engine.renderer import Renderer
from model.audio_model import AudioModel, AudioParameters
from model.video_model import VideoModel, VideoParameters


class Generator:
    def __init__(self) -> None:
        self.video_model = VideoModel()
        self.audio_model = AudioModel()
        self.renderer = Renderer()

    def generate_video(
        self,
        prompt: str,
        output_path: Path,
        resolution: str,
        fps: int,
        duration: int,
        motion_strength: float,
        interpolation: bool,
    ) -> Path:
        metadata = self.video_model.infer(
            prompt,
            VideoParameters(
                resolution=resolution,
                fps=fps,
                duration=duration,
                motion_strength=motion_strength,
                interpolation=interpolation,
            ),
        )
        return self.renderer.render_mp4(output_path, metadata)

    def generate_audio(
        self,
        transcript: str,
        output_path: Path,
        duration: int,
        language: str,
        include_music: bool = True,
        include_voice: bool = True,
    ) -> Path:
        metadata = self.audio_model.synthesize(
            transcript,
            AudioParameters(
                duration=duration,
                language=language,
                include_music=include_music,
                include_voice=include_voice,
            ),
        )
        return self.renderer.render_wav(output_path, metadata)
