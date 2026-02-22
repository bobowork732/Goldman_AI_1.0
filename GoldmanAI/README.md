# Goldman AI 1.0 (Safe Mode)

Goldman AI is a modular Python application that demonstrates a **safe AI video model builder (v1.0)** with:

- Text-to-video generation with post-process flow: blur -> sharp -> result
- Image-to-video animation flow
- Native synchronized audio generation (TTS + sound + mixed export) with waveform validation during mix
- Video/audio mux export that combines generated video and mixed audio
- Prompt understanding parser
- Safety filtering with blocked prompt logging

## Run

```bash
cd GoldmanAI
python main.py
```

> If a desktop display is unavailable, the app automatically falls back to a CLI smoke generation run.

## Key Safety Features

- `safety/filter.py` provides a `safe_generate()` wrapper that validates prompts before generation.
- `safety/moderation.py` checks prompt content against policy rules in `safety/rules.json`.
- Unsafe prompts are blocked and appended to `logs/safety_log.txt`.
- Optional parental/education mode adds stricter blocked terms.

## Architecture

- `model/`: video/audio model abstractions + prompt tokenizer
- `engine/`: generation orchestration, rendering, scheduling, and pipeline wiring
- `ui/`: Tkinter desktop app with controls and settings panel
- `safety/`: moderation rules and filtering logic
- `utils/`: app configuration and environment bootstrap

## Output Files (v1)

Each generation now exports versioned files:

- `generated_video_v1.mp4`
- `generated_tts_v1.wav`
- `generated_sound_v1.wav`
- `generated_audio_v1.wav` (mix of TTS + sound)
- `generated_video_with_audio_v1.mp4` (video + mixed audio result)

## Example Prompts

- `A cinematic sunrise over mountains with slow pan, realistic style, wide camera`
- `A cozy reading room at night with soft lighting and gentle motion`
- `Animate this still image into a slow orbit shot with documentary style`

## Notes

- MP4 export is represented as a dependency-free pseudo MP4 text payload for portability in minimal environments.
- WAV exports are generated as valid synchronized audio tracks in a dependency-free waveform pipeline.
