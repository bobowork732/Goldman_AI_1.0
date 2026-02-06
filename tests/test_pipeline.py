import unittest

from goldman_ai import GoldmanAiPipeline, GoldmanAiStudio


class PipelineTests(unittest.TestCase):
    def test_prompt_sanitization_marks_prompt(self) -> None:
        pipeline = GoldmanAiPipeline()
        understanding = pipeline.analyze_prompt("cinematic city scene with blood")
        self.assertTrue(understanding.sanitized)
        self.assertNotIn("blood", understanding.intent.lower())

    def test_text_to_video_default_frame_count(self) -> None:
        pipeline = GoldmanAiPipeline()
        project = pipeline.text_to_video("cinematic city sunset")
        self.assertEqual(len(project.frames), 192)

    def test_export_manifest_structure(self) -> None:
        studio = GoldmanAiStudio()
        project = studio.create_text_project("city sunset cinematic shot")
        manifest = studio.compile_project(project)
        self.assertIn("video", manifest)
        self.assertIn("audio", manifest)
        self.assertIn("metadata", manifest)
        self.assertTrue(str(manifest["video"][0]).endswith("scene_01_4K.mp4"))

    def test_multilingual_filters_unsupported_language(self) -> None:
        studio = GoldmanAiStudio()
        project = studio.create_multilingual_project(
            prompt="cinematic skyline",
            transcript="hello",
            languages=["en", "es", "xx"],
        )
        languages = [track.language for track in project.audio_tracks]
        self.assertEqual(languages, ["en", "es"])


if __name__ == "__main__":
    unittest.main()
