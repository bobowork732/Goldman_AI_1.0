"""Main pipeline tying safety + prompt parser + generator."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from engine.generator import Generator
from model.tokenizer import PromptTokenizer
from safety.filter import SafetyFilter
from safety.moderation import Moderator
from utils.config import CONFIG


@dataclass
class GenerationRequest:
    prompt: str
    image_path: str | None = None
    fps: int = CONFIG.default_fps
    duration: int = CONFIG.default_duration
    motion_strength: float = CONFIG.default_motion_strength
    interpolation: bool = True
    resolution: str = CONFIG.default_resolution
    parental_mode: bool = CONFIG.parental_mode_default


class GoldmanPipeline:
    def __init__(self) -> None:
        self.tokenizer = PromptTokenizer()
        self.generator = Generator()
        self.safety_filter = SafetyFilter(CONFIG.safety_rules, CONFIG.safety_log)
        self.moderator = Moderator(self.safety_filter)

    def safe_generate(self, request: GenerationRequest) -> dict:
        """Validate prompt then perform safe generation."""
        decision = self.moderator.moderate_prompt(request.prompt, parental_mode=request.parental_mode)
        safe_prompt = decision.result.sanitized_prompt
        features = self.tokenizer.parse(safe_prompt)

        mode = "image_to_video" if request.image_path else "text_to_video"
        stem = "image_scene" if request.image_path else "text_scene"

        video_path = CONFIG.output_dir / f"{stem}.mp4"
        audio_path = CONFIG.output_dir / f"{stem}.wav"

        self.generator.generate_video(
            prompt=features.scene,
            output_path=video_path,
            resolution=request.resolution,
            fps=request.fps,
            duration=request.duration,
            motion_strength=request.motion_strength,
            interpolation=request.interpolation,
        )
        self.generator.generate_audio(
            transcript=f"Narration for: {features.scene}",
            output_path=audio_path,
            duration=request.duration,
            language="en",
        )

        return {
            "approved": decision.approved,
            "mode": mode,
            "safe_prompt": safe_prompt,
            "features": features,
            "video": str(video_path),
            "audio": str(audio_path),
            "blocked_terms": decision.result.blocked_terms,
        }
