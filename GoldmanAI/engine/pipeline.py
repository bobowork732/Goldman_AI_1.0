"""Main pipeline wiring for safe audio+video generation."""

from __future__ import annotations

from dataclasses import dataclass

from .generator import Generator, GenerationResult
from .renderer import Renderer
from ..model.audio_model import AudioModel
from ..model.video_model import VideoModel
from ..safety.filter import SafetyFilter
from ..safety.moderation import SafetyModerator
from ..utils.config import AppConfig, DEFAULT_CONFIG


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

    def safe_generate(
        self,
        prompt: str,
        source_image: str | None = None,
        duration_seconds: int | None = None,
        audio_enabled: bool = True,
        multi_shot_enabled: bool = False,
        lip_sync_enabled: bool = False,
        lip_sync_focus: bool = False,
        parental_education_mode: bool | None = None,
    ) -> GenerationResult:
        """Validate prompt then run text-to-video or image-to-video generation."""
        chosen_duration = duration_seconds if duration_seconds is not None else self.config.render.duration_seconds
        chosen_parental_mode = (
            parental_education_mode
            if parental_education_mode is not None
            else self.config.safety.parental_education_mode
        )
        return self.safety_filter.safe_generate(
            prompt,
            self.generator.generate,
            output_dir=self.config.assets_output_dir,
            fps=self.config.render.fps,
            duration_seconds=chosen_duration,
            motion_strength=self.config.render.motion_strength,
            frame_interpolation=self.config.render.frame_interpolation,
            source_image=source_image,
            audio_enabled=audio_enabled,
            multi_shot_enabled=multi_shot_enabled,
            lip_sync_enabled=lip_sync_enabled,
            lip_sync_focus=lip_sync_focus,
            parental_education_mode=chosen_parental_mode,
        )
