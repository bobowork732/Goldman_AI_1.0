# Goldman AI 1.0 (Safe Mode)

Goldman AI is a modular Python application that demonstrates a **safe AI video model builder** with:

- Text-to-video generation
- Image-to-video animation flow
- Native synchronized audio generation
- Prompt understanding parser
- Safety filtering with blocked prompt logging

## Run

```bash
cd GoldmanAI
python main.py
```

> If a desktop display is unavailable, the app automatically falls back to a CLI smoke generation run.

## Web App (Frontend + Backend)

A built-in web interface is available with:

- Frontend studio page (`/`) with animated image AI input support, preview, download buttons, duration presets (6s/10s/15s/20s), audio on/off, multi-shot on/off, and lip-sync + focus lip-sync switches
- Backend JSON API (`/api/health`, `/api/generate`) returning video/audio/mix output URLs and settings metadata (including lip-sync state)
- Terms of Service page (`/terms`)

Run it from the repository root:

```bash
python -m GoldmanAI.web.server
```

Then open `http://localhost:8080` to generate, preview, and download video/audio outputs.

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

## Example Prompts

- `A cinematic sunrise over mountains with slow pan, realistic style, wide camera`
- `A cozy reading room at night with soft lighting and gentle motion`
- `Animate this still image into a slow orbit shot with documentary style`

## Notes

- MP4 export is represented as a dependency-free pseudo MP4 text payload for portability in minimal environments.
- WAV export is generated as a valid silent audio track synchronized to configured duration.
