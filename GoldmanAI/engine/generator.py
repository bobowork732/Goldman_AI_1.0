"""Generation orchestration for text-to-video and image-to-video."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from model.video_model import VideoModel, VideoParams
from model.audio_model import AudioModel
from model.tokenizer import PromptTokenizer
from engine.renderer import Renderer
from engine.scheduler import FrameScheduler


@dataclass(slots=True)
class GenerationResult:
    video_path: Path
    audio_path: Path
    tts_audio_path: Path
    sound_audio_path: Path
    parsed_prompt: dict[str, str]
    model_version: str


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

        frames = self.video_model.infer_frames(params, source_image=source_image)
        processed_frames = self.scheduler.run(lambda frame: frame, frames)
        final_frames = self.renderer.interpolate_frames(processed_frames, enabled=frame_interpolation)

        video_path = self.renderer.export_mp4(final_frames, output_dir / "generated_video_v1.mp4", fps=fps)
        tts_audio_path = self.audio_model.synthesize_tts(prompt, duration_seconds, output_dir / "generated_tts_v1.wav")
        sound_audio_path = self.audio_model.synthesize_soundtrack(prompt, duration_seconds, output_dir / "generated_sound_v1.wav")
        audio_path = self.audio_model.mix_audio(tts_audio_path, sound_audio_path, output_dir / "generated_audio_v1.wav")

        model_version = self.video_model.VERSION
        return GenerationResult(
            video_path=video_path,
            audio_path=audio_path,
            tts_audio_path=tts_audio_path,
            sound_audio_path=sound_audio_path,
            parsed_prompt={
                "scene": parsed.scene,
                "lighting": parsed.lighting,
                "motion": parsed.motion,
                "style": parsed.style,
                "camera_type": parsed.camera_type,
            },
            model_version=model_version,
        )
