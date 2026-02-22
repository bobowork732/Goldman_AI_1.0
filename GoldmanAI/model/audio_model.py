"""Native audio synthesis model abstraction with TTS + sound mixing."""

from __future__ import annotations

from array import array
from pathlib import Path
import math
import wave


class AudioModel:
    """Synthesizes separate TTS and sound tracks, then mixes them into one audio file."""

    def __init__(self, sample_rate: int = 22050) -> None:
        self.sample_rate = sample_rate

    def synthesize_tts(self, prompt: str, duration_seconds: int, output_path: Path) -> Path:
        """Create a synthetic TTS-like waveform whose cadence depends on prompt length."""
        total_samples = max(1, duration_seconds * self.sample_rate)
        base_freq = 160 + (len(prompt) % 140)
        volume = 4200
        samples = array(
            "h",
            (
                int(volume * math.sin(2 * math.pi * base_freq * i / self.sample_rate))
                for i in range(total_samples)
            ),
        )
        self._write_wav(samples, output_path)
        return output_path

    def synthesize_soundtrack(self, prompt: str, duration_seconds: int, output_path: Path) -> Path:
        """Create a synthetic ambient soundtrack waveform."""
        total_samples = max(1, duration_seconds * self.sample_rate)
        atmosphere_freq = 70 + (sum(ord(ch) for ch in prompt) % 90)
        volume = 2600
        samples = array(
            "h",
            (
                int(volume * math.sin(2 * math.pi * atmosphere_freq * i / self.sample_rate))
                for i in range(total_samples)
            ),
        )
        self._write_wav(samples, output_path)
        return output_path

    def mix_audio(self, tts_path: Path, sound_path: Path, output_path: Path) -> Path:
        """Mix two mono tracks by averaging sample values and clipping safely."""
        tts = self._read_wav(tts_path)
        sound = self._read_wav(sound_path)
        mixed_length = min(len(tts), len(sound))
        mixed = array("h")

        for idx in range(mixed_length):
            value = int((tts[idx] * 0.65) + (sound[idx] * 0.75))
            if value > 32767:
                value = 32767
            elif value < -32768:
                value = -32768
            mixed.append(value)

        self._write_wav(mixed, output_path)
        return output_path

    def synthesize(self, prompt: str, duration_seconds: int, output_path: Path) -> Path:
        """Compatibility method: produce mixed output while keeping v1 API."""
        base_dir = output_path.parent
        tts_path = base_dir / "generated_tts_v1.wav"
        sound_path = base_dir / "generated_sound_v1.wav"

        self.synthesize_tts(prompt, duration_seconds, tts_path)
        self.synthesize_soundtrack(prompt, duration_seconds, sound_path)
        return self.mix_audio(tts_path, sound_path, output_path)

    def _write_wav(self, samples: array, output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with wave.open(str(output_path), "w") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(samples.tobytes())

    def _read_wav(self, input_path: Path) -> array:
        with wave.open(str(input_path), "r") as wf:
            raw = wf.readframes(wf.getnframes())
        return array("h", raw)
