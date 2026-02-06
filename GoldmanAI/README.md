# Goldman AI v1.0

Safe, modular Python video-generation scaffold supporting:

- Text → Video
- Image → Video
- Native audio synthesis (voice + music metadata)
- Prompt understanding engine
- Desktop UI (`python main.py`)
- Safety filter with logging and safe generation wrapper

## Run

```bash
pip install -r requirements.txt
python main.py
```

## Safety

- Prompt filtering rules: `safety/rules.json`
- Safety log file: `logs/safety_log.txt`
- `safe_generate()` validates/sanitizes prompts before generation.
- Optional parental/education mode available in the UI settings and pipeline request.

## Example prompts

- `Cinematic city sunset with people walking and warm lighting`
- `A realistic mountain valley with soft morning fog and slow camera dolly`
- `Animate this image into a calm nature timelapse with smooth motion`

## Notes

This version writes placeholder `.mp4` and `.wav` artifacts with metadata payloads so the app is runnable in lightweight environments. Replace `engine/renderer.py` with real encoders for production media output.
