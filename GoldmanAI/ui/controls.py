"""Tkinter controls for Goldman AI UI."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class SettingsPanel(ttk.LabelFrame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, text="Settings")

        self.safety_mode = tk.BooleanVar(value=False)
        self.resolution = tk.StringVar(value="1920x1080")
        self.render_speed = tk.StringVar(value="balanced")

        ttk.Checkbutton(self, text="Parental/Education Safety Mode", variable=self.safety_mode).grid(
            row=0, column=0, sticky="w", padx=6, pady=4
        )
        ttk.Label(self, text="Resolution").grid(row=1, column=0, sticky="w", padx=6)
        ttk.Combobox(self, textvariable=self.resolution, values=["1280x720", "1920x1080", "3840x2160"]).grid(
            row=2, column=0, sticky="ew", padx=6, pady=4
        )
        ttk.Label(self, text="Render Speed").grid(row=3, column=0, sticky="w", padx=6)
        ttk.Combobox(self, textvariable=self.render_speed, values=["quality", "balanced", "fast"]).grid(
            row=4, column=0, sticky="ew", padx=6, pady=4
        )
        self.columnconfigure(0, weight=1)
