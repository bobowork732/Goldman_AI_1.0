"""Entrypoint for Goldman AI application."""

from __future__ import annotations

from engine.pipeline import GoldmanPipeline
from ui.app_ui import GoldmanAppUI
from utils.loader import prepare_environment


def main() -> None:
    prepare_environment()
    pipeline = GoldmanPipeline()
    try:
        app = GoldmanAppUI(pipeline)
        app.run()
    except Exception as exc:
        # Headless fallback keeps `python main.py` functional in no-display environments.
        print("UI unavailable, running safe CLI smoke generation instead:", exc)
        result = pipeline.safe_generate("A realistic forest trail at sunrise with slow pan")
        print(f"Generated video: {result.video_path}")
        print(f"Generated audio: {result.audio_path}")


if __name__ == "__main__":
    main()
