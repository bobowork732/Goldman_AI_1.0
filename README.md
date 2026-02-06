# Goldman Ai v1.0 (Safe Production Template)

Goldman Ai is a cinematic video-generation scaffold for:

- **Text-to-video**
- **Image-to-video**
- **Frame-by-frame generation**
- **Built-in audio + multilingual audio layers**
- **Prompt understanding with structured scene planning**
- **Safety-first sanitization for general-audience outputs**

## Safety core behavior

Goldman Ai v1.0 automatically sanitizes unsafe prompts into safe cinematic alternatives and keeps outputs focused on respectful, non-harmful scenes.

## Default rendering mode

Unless overridden, the pipeline uses:

- Resolution: **4K**
- Frame rate: **24fps**
- Lighting: **cinematic HDR**
- Color grading: **filmic natural tones**
- Camera motion: **smooth stabilized movement**
- Duration: **5-10 seconds** (default modeled as ~8s)

## Structured scene understanding

Prompt interpretation is represented with:

1. Environment (location, weather, lighting, time of day)
2. Subject (count, clothing/materials, expression, movement)
3. Camera (lens, focal length, motion, framing)
4. Motion physics (gravity, interactions, cloth/hair behavior)
5. Audio (ambience, music mood, effects)

## GoldmanAI_Project output mapping

`compile_project()` returns a manifest aligned to:

```text
/GoldmanAI_Project
    /video
        scene_01_4K.mp4
        scene_02_4K.mp4
    /audio
        scene_01.wav
        ambience.wav
    /frames
        frame_0001.png
        frame_0002.png
    /metadata
        prompt.txt
        camera_data.json
        lighting.json
```

## Example usage

```python
from goldman_ai import GoldmanAiStudio

studio = GoldmanAiStudio()
project = studio.create_multilingual_project(
    prompt="City sunset cinematic shot with people walking",
    transcript="Welcome to Goldman AI.",
    languages=["en", "es", "fr"],
)
manifest = studio.compile_project(project)
print(manifest)
```
