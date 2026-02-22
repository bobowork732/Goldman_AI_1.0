"""Tkinter UI for Goldman AI generation workflow."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from engine.pipeline import GoldmanPipeline
from safety.filter import SafeGenerationError
from ui.controls import UISettings


class GoldmanAppUI:
    """Desktop application with prompt input, preview, and export controls."""

    def __init__(self, pipeline: GoldmanPipeline) -> None:
        self.pipeline = pipeline
        self.settings = UISettings()
        self.last_video_path: str | None = None
        self.last_audio_path: str | None = None
        self.last_tts_audio_path: str | None = None
        self.last_sound_audio_path: str | None = None

        self.root = tk.Tk()
        self.root.title("Goldman AI Video Builder")
        self.root.geometry("900x600")

        self.prompt_var = tk.StringVar(value="A cinematic sunrise over mountains with slow pan")
        self.source_image_var = tk.StringVar(value="")
        self.preview_var = tk.StringVar(value="No output generated yet.")
        self.safety_mode_var = tk.BooleanVar(value=self.settings.safety_mode)
        self.resolution_var = tk.StringVar(value=self.settings.resolution)
        self.speed_var = tk.StringVar(value=self.settings.render_speed)

        self._build_layout()

    def _build_layout(self) -> None:
        frame = tk.Frame(self.root, padx=12, pady=12)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Prompt").pack(anchor="w")
        tk.Entry(frame, textvariable=self.prompt_var, width=110).pack(fill=tk.X)

        tk.Label(frame, text="Optional source image path (for image→video)").pack(anchor="w", pady=(8, 0))
        tk.Entry(frame, textvariable=self.source_image_var, width=110).pack(fill=tk.X)

        button_row = tk.Frame(frame)
        button_row.pack(fill=tk.X, pady=10)
        tk.Button(button_row, text="Generate", command=self.generate).pack(side=tk.LEFT)
        tk.Button(button_row, text="Export", command=self.export).pack(side=tk.LEFT, padx=8)

        settings = tk.LabelFrame(frame, text="Settings")
        settings.pack(fill=tk.X, pady=8)
        tk.Checkbutton(settings, text="Parental/Education Safety Mode", variable=self.safety_mode_var).pack(anchor="w")
        tk.Label(settings, text="Resolution").pack(anchor="w")
        tk.Entry(settings, textvariable=self.resolution_var).pack(fill=tk.X)
        tk.Label(settings, text="Render speed").pack(anchor="w")
        tk.Entry(settings, textvariable=self.speed_var).pack(fill=tk.X)

        tk.Label(frame, text="Preview").pack(anchor="w", pady=(10, 0))
        tk.Label(frame, textvariable=self.preview_var, justify="left", anchor="w", bg="#f5f5f5", padx=8, pady=8).pack(fill=tk.BOTH, expand=True)

    def generate(self) -> None:
        self.pipeline.config.safety.parental_education_mode = bool(self.safety_mode_var.get())
        self.pipeline.config.render.render_speed = self.speed_var.get().strip() or "balanced"

        prompt = self.prompt_var.get().strip()
        source = self.source_image_var.get().strip() or None
        try:
            result = self.pipeline.safe_generate(prompt, source_image=source)
        except SafeGenerationError as exc:
            messagebox.showerror("Blocked by safety filter", str(exc))
            return
        except Exception as exc:  # pragma: no cover
            messagebox.showerror("Generation error", str(exc))
            return

        self.last_video_path = str(result.video_path)
        self.last_audio_path = str(result.audio_path)
        self.last_tts_audio_path = str(result.tts_audio_path)
        self.last_sound_audio_path = str(result.sound_audio_path)

        self.preview_var.set(
            "\n".join(
                [
                    f"Video: {self.last_video_path}",
                    f"Audio (mixed): {self.last_audio_path}",
                    f"TTS track: {self.last_tts_audio_path}",
                    f"Sound track: {self.last_sound_audio_path}",
                    f"Parsed prompt: {result.parsed_prompt}",
                    f"GPU enabled: {self.pipeline.state.using_gpu}",
                ]
            )
        )

    def export(self) -> None:
        if not self.last_video_path:
            messagebox.showinfo("Nothing to export", "Generate content first.")
            return
        messagebox.showinfo(
            "Export complete",
            f"Video saved to: {self.last_video_path}\n"
            f"Mixed audio saved to: {self.last_audio_path}\n"
            f"TTS audio saved to: {self.last_tts_audio_path}\n"
            f"Sound audio saved to: {self.last_sound_audio_path}",
        )

    def run(self) -> None:
        self.root.mainloop()
