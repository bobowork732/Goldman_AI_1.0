"""Core pipeline scaffolding for Goldman Ai v1.0 safe production template."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List, Mapping, Sequence


UNSAFE_TERMS = {
    "kill",
    "murder",
    "blood",
    "torture",
    "bomb",
    "weapon",
    "drugs",
    "explicit",
    "porn",
    "self-harm",
    "suicide",
}


@dataclass(frozen=True)
class Frame:
    """Represents a single video frame in the project timeline."""

    index: int
    description: str
    source: str
    timestamp_s: float


@dataclass(frozen=True)
class AudioTrack:
    """Represents an audio layer (voice, music, or SFX) in the timeline."""

    language: str
    transcript: str
    style: str
    role: str
    file_name: str


@dataclass(frozen=True)
class EnvironmentSpec:
    """Environment understanding extracted from prompt/template."""

    location: str
    weather: str
    lighting: str
    time_of_day: str


@dataclass(frozen=True)
class SubjectSpec:
    """Subject understanding extracted from prompt/template."""

    count: str
    clothing_materials: str
    expression: str
    movement: str


@dataclass(frozen=True)
class CameraSpec:
    """Camera understanding extracted from prompt/template."""

    lens_type: str
    focal_length: str
    motion: str
    framing: str


@dataclass(frozen=True)
class MotionPhysicsSpec:
    """Physical consistency guidance for rendering."""

    gravity_consistency: str
    object_interaction: str
    cloth_hair_simulation: str


@dataclass(frozen=True)
class AudioSpec:
    """Audio intent for ambience/music/effects."""

    ambience: str
    background_music_mood: str
    sound_effects: str


@dataclass(frozen=True)
class PromptUnderstanding:
    """Structured understanding extracted from a prompt."""

    intent: str
    style: str
    key_entities: Sequence[str]
    references: Sequence[str]
    environment: EnvironmentSpec
    subject: SubjectSpec
    camera: CameraSpec
    motion_physics: MotionPhysicsSpec
    audio: AudioSpec
    sanitized: bool


@dataclass(frozen=True)
class ScenePlan:
    """Represents a planned scene derived from prompt understanding."""

    scene_id: int
    file_stem: str
    description: str
    duration_s: float


@dataclass(frozen=True)
class RenderSettings:
    """Default Goldman AI rendering mode settings."""

    resolution: str = "4K"
    fps: int = 24
    lighting_mode: str = "cinematic HDR"
    color_grading: str = "filmic natural tones"
    camera_stabilization: str = "smooth stabilized movement"
    duration_s: float = 8.0
    format: str = "mp4"


@dataclass(frozen=True)
class AudioPolicy:
    """Represents policy defaults for audio generation."""

    default_language: str = "en"
    supported_languages: Sequence[str] = (
        "en",
        "es",
        "fr",
        "de",
        "pt",
        "hi",
        "ar",
        "ja",
        "ko",
        "zh",
    )
    default_style: str = "cinematic"


@dataclass
class VideoProject:
    """Aggregates generated frames, audio, and planning artifacts."""

    title: str
    prompt: str
    frames: List[Frame] = field(default_factory=list)
    audio_tracks: List[AudioTrack] = field(default_factory=list)
    prompt_understanding: PromptUnderstanding | None = None
    scene_plan: List[ScenePlan] = field(default_factory=list)

    def add_frames(self, new_frames: Iterable[Frame]) -> None:
        self.frames.extend(new_frames)

    def add_audio(self, tracks: Iterable[AudioTrack]) -> None:
        self.audio_tracks.extend(tracks)

    def add_scenes(self, scenes: Iterable[ScenePlan]) -> None:
        self.scene_plan.extend(scenes)


class GoldmanAiPipeline:
    """High-level pipeline for safe multi-modal video generation."""

    def __init__(
        self,
        model_name: str = "Goldman Ai",
        version: str = "1.0",
        render_settings: RenderSettings | None = None,
    ) -> None:
        self.model_name = model_name
        self.version = version
        self.render_settings = render_settings or RenderSettings()

    def text_to_video(self, prompt: str, frame_count: int | None = None) -> VideoProject:
        """Create a video project from a text prompt."""
        project = VideoProject(title=f"{self.model_name} Text-to-Video", prompt=prompt)
        project.prompt_understanding = self.analyze_prompt(prompt)
        project.add_scenes(self.plan_scenes(project.prompt_understanding))
        final_frame_count = frame_count or int(self.render_settings.fps * self.render_settings.duration_s)
        project.add_frames(
            self._build_frames(
                source="text",
                description=project.prompt_understanding.intent,
                frame_count=final_frame_count,
                fps=self.render_settings.fps,
            )
        )
        return project

    def image_to_video(self, image_path: str, prompt: str, frame_count: int | None = None) -> VideoProject:
        """Create a video project from an input image and guiding prompt."""
        project = VideoProject(title=f"{self.model_name} Image-to-Video", prompt=prompt)
        project.prompt_understanding = self.analyze_prompt(prompt)
        project.add_scenes(self.plan_scenes(project.prompt_understanding))
        description = f"Image seed: {image_path}. Prompt: {project.prompt_understanding.intent}"
        final_frame_count = frame_count or int(self.render_settings.fps * self.render_settings.duration_s)
        project.add_frames(
            self._build_frames(
                source="image",
                description=description,
                frame_count=final_frame_count,
                fps=self.render_settings.fps,
            )
        )
        return project

    def frame_by_frame(
        self,
        frame_prompts: Sequence[str],
        source: str = "frame-by-frame",
        fps: int = 24,
    ) -> VideoProject:
        """Create a project with explicit per-frame descriptions."""
        project = VideoProject(title=f"{self.model_name} Frame-by-Frame", prompt="Frame-by-frame sequence")
        sanitized_prompts = [self._sanitize_prompt(p) for p in frame_prompts]
        frames = [
            Frame(
                index=index,
                description=prompt,
                source=source,
                timestamp_s=(index - 1) / fps,
            )
            for index, prompt in enumerate(sanitized_prompts, start=1)
        ]
        project.add_frames(frames)
        return project

    def add_audio_layers(
        self,
        project: VideoProject,
        transcript: str,
        language: str = "en",
        style: str = "cinematic",
        role: str = "narration",
        file_name: str | None = None,
    ) -> None:
        """Attach an audio layer to an existing project."""
        safe_transcript = self._sanitize_prompt(transcript)
        audio_name = file_name or "scene_01.wav"
        project.add_audio(
            [
                AudioTrack(
                    language=language,
                    transcript=safe_transcript,
                    style=style,
                    role=role,
                    file_name=audio_name,
                )
            ]
        )

    def multilingual_audio(
        self,
        project: VideoProject,
        transcript: str,
        languages: Sequence[str],
        style: str = "cinematic",
        role: str = "narration",
    ) -> None:
        """Add the same narration in multiple languages."""
        safe_transcript = self._sanitize_prompt(transcript)
        tracks = [
            AudioTrack(
                language=language,
                transcript=safe_transcript,
                style=style,
                role=role,
                file_name=f"scene_01_{language}.wav",
            )
            for language in languages
        ]
        project.add_audio(tracks)

    def analyze_prompt(self, prompt: str) -> PromptUnderstanding:
        """Extract structured understanding from the user prompt."""
        safe_prompt = self._sanitize_prompt(prompt)
        tokens = [token.strip(",.!?") for token in safe_prompt.split()]
        key_entities = [token for token in tokens if token.istitle()][:5]
        references = [token for token in tokens if token.startswith("#")]
        style = "photorealistic cinematic film" if "cinematic" in safe_prompt.lower() else "neutral"

        env = EnvironmentSpec(
            location="modern city" if "city" in safe_prompt.lower() else "unspecified location",
            weather="clear",
            lighting="sunset orange lighting" if "sunset" in safe_prompt.lower() else "cinematic HDR",
            time_of_day="sunset" if "sunset" in safe_prompt.lower() else "day",
        )
        subject = SubjectSpec(
            count="multiple" if "people" in safe_prompt.lower() else "single",
            clothing_materials="natural fabric",
            expression="neutral",
            movement="walking naturally" if "walking" in safe_prompt.lower() else "stable natural motion",
        )
        camera = CameraSpec(
            lens_type="cinema prime",
            focal_length="35mm",
            motion="slow cinematic dolly movement",
            framing="medium wide",
        )
        physics = MotionPhysicsSpec(
            gravity_consistency="enforced",
            object_interaction="physically plausible",
            cloth_hair_simulation="enabled",
        )
        audio = AudioSpec(
            ambience="distant city ambience" if "city" in safe_prompt.lower() else "soft natural ambience",
            background_music_mood="inspiring cinematic",
            sound_effects="subtle environmental effects",
        )
        return PromptUnderstanding(
            intent=safe_prompt,
            style=style,
            key_entities=key_entities or ["subject"],
            references=references,
            environment=env,
            subject=subject,
            camera=camera,
            motion_physics=physics,
            audio=audio,
            sanitized=safe_prompt != prompt,
        )

    def plan_scenes(self, understanding: PromptUnderstanding) -> List[ScenePlan]:
        """Create a scene plan from prompt understanding."""
        return [
            ScenePlan(
                scene_id=1,
                file_stem="scene_01",
                description=f"{understanding.style}; {understanding.environment.location}; {understanding.camera.motion}",
                duration_s=5.0,
            ),
            ScenePlan(
                scene_id=2,
                file_stem="scene_02",
                description=f"{understanding.subject.movement}; {understanding.audio.ambience}",
                duration_s=5.0,
            ),
        ]

    def export_manifest(self, project: VideoProject, root: str = "GoldmanAI_Project") -> Mapping[str, object]:
        """Return output structure manifest using Goldman AI project conventions."""
        root_path = Path(root)
        scene_files = [f"{scene.file_stem}_{self.render_settings.resolution}.{self.render_settings.format}" for scene in project.scene_plan]
        audio_files = [track.file_name for track in project.audio_tracks] or ["scene_01.wav", "ambience.wav"]

        return {
            "root": str(root_path),
            "video": [str(root_path / "video" / file_name) for file_name in scene_files],
            "audio": [str(root_path / "audio" / file_name) for file_name in audio_files],
            "frames": [
                str(root_path / "frames" / f"frame_{frame.index:04d}.png")
                for frame in project.frames[:2]
            ],
            "metadata": {
                "prompt": str(root_path / "metadata" / "prompt.txt"),
                "camera_data": str(root_path / "metadata" / "camera_data.json"),
                "lighting": str(root_path / "metadata" / "lighting.json"),
            },
            "render": {
                "resolution": self.render_settings.resolution,
                "fps": self.render_settings.fps,
                "lighting": self.render_settings.lighting_mode,
                "color_grading": self.render_settings.color_grading,
                "camera": self.render_settings.camera_stabilization,
            },
        }

    def _build_frames(
        self, source: str, description: str, frame_count: int, fps: int
    ) -> List[Frame]:
        """Create placeholder frames with metadata for each step in the timeline."""
        return [
            Frame(
                index=index,
                description=description,
                source=source,
                timestamp_s=(index - 1) / fps,
            )
            for index in range(1, frame_count + 1)
        ]

    def _sanitize_prompt(self, prompt: str) -> str:
        """Replace unsafe terms with safe cinematic alternatives."""
        clean_prompt = prompt
        for term in UNSAFE_TERMS:
            clean_prompt = clean_prompt.replace(term, "safe cinematic moment")
            clean_prompt = clean_prompt.replace(term.capitalize(), "Safe cinematic moment")
        return clean_prompt


class GoldmanAiStudio:
    """Convenience wrapper that manages policies and render settings."""

    def __init__(
        self,
        pipeline: GoldmanAiPipeline | None = None,
        audio_policy: AudioPolicy | None = None,
        render_settings: RenderSettings | None = None,
    ) -> None:
        self.pipeline = pipeline or GoldmanAiPipeline(render_settings=render_settings)
        self.audio_policy = audio_policy or AudioPolicy()
        self.render_settings = render_settings or RenderSettings()

    def create_text_project(self, prompt: str) -> VideoProject:
        """Create a text-to-video project using default policies."""
        project = self.pipeline.text_to_video(prompt)
        if not project.audio_tracks:
            self.pipeline.add_audio_layers(
                project,
                transcript="Welcome to Goldman AI.",
                language=self.audio_policy.default_language,
                style=self.audio_policy.default_style,
                file_name="scene_01.wav",
            )
        return project

    def create_multilingual_project(
        self, prompt: str, transcript: str, languages: Sequence[str]
    ) -> VideoProject:
        """Create a text project with multilingual narration."""
        project = self.pipeline.text_to_video(prompt)
        allowed_languages = [
            language
            for language in languages
            if language in self.audio_policy.supported_languages
        ]
        self.pipeline.multilingual_audio(
            project,
            transcript=transcript,
            languages=allowed_languages,
            style=self.audio_policy.default_style,
            role="narration",
        )
        return project

    def compile_project(self, project: VideoProject) -> Mapping[str, object]:
        """Return a render/export manifest that can be handed to a renderer."""
        return self.pipeline.export_manifest(project)
