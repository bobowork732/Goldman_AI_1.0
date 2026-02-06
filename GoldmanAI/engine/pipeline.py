"""Main pipeline wiring for safe audio+video generation."""

from __future__ import annotations

from dataclasses import dataclass

from engine.generator import Generator, GenerationResult
from engine.renderer import Renderer
from model.audio_model import AudioModel
from model.video_model import VideoModel
from safety.filter import SafetyFilter
from safety.moderation import SafetyModerator
from utils.config import AppConfig, DEFAULT_CONFIG


@dataclass(slots=True)
class PipelineState:
    using_gpu: bool


class GoldmanPipeline:
    """Loads models and exposes a unified safe generation API."""

    def __init__(self, config: AppConfig | None = None) -> None:
        self.config = config or DEFAULT_CONFIG
        self.state = PipelineState(using_gpu=self._gpu_available())

        moderator = SafetyModerator(self.config.project_root / "safety" / "rules.json")
        self.safety_filter = SafetyFilter(moderator, self.config.safety_log_file)

        self.generator = Generator(
            video_model=VideoModel(use_gpu=self.state.using_gpu),
            audio_model=AudioModel(),
            renderer=Renderer(),
        )

    @staticmethod
    def _gpu_available() -> bool:
        try:
            import torch  # type: ignore

            return bool(torch.cuda.is_available())
        except Exception:
            return False

    def safe_generate(self, prompt: str, source_image: str | None = None) -> GenerationResult:
        """Validate prompt then run text-to-video or image-to-video generation."""
        return self.safety_filter.safe_generate(
            prompt,
            self.generator.generate,
            output_dir=self.config.assets_output_dir,
            fps=self.config.render.fps,
            duration_seconds=self.config.render.duration_seconds,
            motion_strength=self.config.render.motion_strength,
            frame_interpolation=self.config.render.frame_interpolation,
            source_image=source_image,
            parental_education_mode=self.config.safety.parental_education_mode,
        )
