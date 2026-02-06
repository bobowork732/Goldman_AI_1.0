"""Simple usage demo for Goldman Ai v1.0 safe production template."""

from goldman_ai import GoldmanAiStudio


def main() -> None:
    studio = GoldmanAiStudio()
    project = studio.create_multilingual_project(
        prompt="City sunset cinematic shot with people walking",
        transcript="Welcome to Goldman AI.",
        languages=["en", "es", "fr", "xx"],
    )
    manifest = studio.compile_project(project)
    print("Render manifest:", manifest)


if __name__ == "__main__":
    main()
