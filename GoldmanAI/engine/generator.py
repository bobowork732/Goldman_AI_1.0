"""Generation orchestration for text-to-video and image-to-video."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..model.video_model import VideoModel, VideoParams
from ..model.audio_model import AudioModel
from ..model.tokenizer import PromptTokenizer
from .renderer import Renderer
from .scheduler import FrameScheduler


@dataclass(slots=True)
class GenerationResult:
    video_path: Path
    audio_path: Path | None
    mix_path: Path
    parsed_prompt: dict[str, str]
    duration_seconds: int
    audio_enabled: bool
    multi_shot_enabled: bool
    lip_sync_enabled: bool
    lip_sync_focus: bool


class Generator:
    """Coordinates model inference and rendering."""

    def __init__(self, video_model: VideoModel, audio_model: AudioModel, renderer: Renderer) -> None:
        self.video_model = video_model
        self.audio_model = audio_model
        self.renderer = renderer
        self.tokenizer = PromptTokenizer()
        self.scheduler = FrameScheduler()

    def generate(
        self,
        prompt: str,
        output_dir: Path,
        fps: int,
        duration_seconds: int,
        motion_strength: float,
        frame_interpolation: bool,
        source_image: str | None = None,
        audio_enabled: bool = True,
        multi_shot_enabled: bool = False,
        lip_sync_enabled: bool = False,
        lip_sync_focus: bool = False,
    ) -> GenerationResult:
        parsed = self.tokenizer.parse(prompt)
        params = VideoParams(
            scene=parsed.scene,
            lighting=parsed.lighting,
            motion=parsed.motion,
            style=parsed.style,
            camera_type=parsed.camera_type,
            fps=fps,
            duration_seconds=duration_seconds,
            motion_strength=motion_strength,
        )

        frames = self.video_model.infer_frames(
            params,
            source_image=source_image,
            multi_shot=multi_shot_enabled,
            lip_sync_enabled=lip_sync_enabled,
            lip_sync_focus=lip_sync_focus,
        )
        processed_frames = self.scheduler.run(lambda frame: frame, frames)
        final_frames = self.renderer.interpolate_frames(processed_frames, enabled=frame_interpolation)

        video_path = self.renderer.export_mp4(final_frames, output_dir / "generated_video.mp4", fps=fps)
        audio_path = None
        if audio_enabled:
            audio_path = self.audio_model.synthesize(prompt, duration_seconds, output_dir / "generated_audio.wav")
        mix_path = self.renderer.export_mix_manifest(video_path, audio_path, output_dir / "generated_mix.txt")

        return GenerationResult(
            video_path=video_path,
            audio_path=audio_path,
            mix_path=mix_path,
            parsed_prompt={
                "scene": parsed.scene,
                "lighting": parsed.lighting,
                "motion": parsed.motion,
                "style": parsed.style,
                "camera_type": parsed.camera_type,
            },
            duration_seconds=duration_seconds,
            audio_enabled=audio_enabled,
            multi_shot_enabled=multi_shot_enabled,
            lip_sync_enabled=lip_sync_enabled,
            lip_sync_focus=lip_sync_focus,
        )
