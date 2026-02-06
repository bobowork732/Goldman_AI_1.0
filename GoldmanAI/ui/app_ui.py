"""Main desktop UI for Goldman AI."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from engine.pipeline import GenerationRequest, GoldmanPipeline
from ui.controls import SettingsPanel


class GoldmanApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Goldman AI v1.0")
        self.geometry("900x600")

        self.pipeline = GoldmanPipeline()

        self.prompt_text = tk.Text(self, height=8)
        self.prompt_text.pack(fill="x", padx=10, pady=10)

        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", padx=10)

        ttk.Button(toolbar, text="Generate", command=self.on_generate).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Export", command=self.on_export).pack(side="left", padx=5)

        self.settings = SettingsPanel(self)
        self.settings.pack(fill="x", padx=10, pady=8)

        self.preview = tk.Text(self, height=20)
        self.preview.pack(fill="both", expand=True, padx=10, pady=10)

        self.last_result: dict | None = None

    def on_generate(self) -> None:
        prompt = self.prompt_text.get("1.0", "end").strip()
        if not prompt:
            messagebox.showwarning("Goldman AI", "Enter a prompt first.")
            return

        request = GenerationRequest(
            prompt=prompt,
            parental_mode=self.settings.safety_mode.get(),
            resolution=self.settings.resolution.get(),
            duration=5,
            fps=24,
            motion_strength=0.6,
            interpolation=True,
        )
        result = self.pipeline.safe_generate(request)
        self.last_result = result

        self.preview.delete("1.0", "end")
        self.preview.insert("end", f"Mode: {result['mode']}\n")
        self.preview.insert("end", f"Safe prompt: {result['safe_prompt']}\n")
        self.preview.insert("end", f"Blocked terms: {result['blocked_terms']}\n")
        self.preview.insert("end", f"Video: {result['video']}\n")
        self.preview.insert("end", f"Audio: {result['audio']}\n")

    def on_export(self) -> None:
        if not self.last_result:
            messagebox.showinfo("Goldman AI", "Generate content first.")
            return
        messagebox.showinfo(
            "Goldman AI",
            f"Exported:\n{self.last_result['video']}\n{self.last_result['audio']}",
        )
