"""Native audio synthesis model abstraction."""

from __future__ import annotations

from pathlib import Path
import wave


class AudioModel:
    """Synthesizes a simple silent WAV track for synchronized exports."""

    def synthesize(self, prompt: str, duration_seconds: int, output_path: Path) -> Path:
        sample_rate = 22050
        nframes = duration_seconds * sample_rate
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with wave.open(str(output_path), "w") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(b"\x00\x00" * nframes)

        return output_path
