import unittest

from engine.pipeline import GenerationRequest, GoldmanPipeline


class SafePipelineTests(unittest.TestCase):
    def test_safe_generate_sanitizes_and_logs_terms(self) -> None:
        pipeline = GoldmanPipeline()
        result = pipeline.safe_generate(GenerationRequest(prompt="cinematic scene with blood"))
        self.assertIn("safe", result["safe_prompt"].lower())
        self.assertIn("blood", result["blocked_terms"])

    def test_parental_mode_applies_additional_rules(self) -> None:
        pipeline = GoldmanPipeline()
        result = pipeline.safe_generate(
            GenerationRequest(prompt="dark cinematic forest", parental_mode=True)
        )
        self.assertNotIn("dark", result["safe_prompt"].lower())


if __name__ == "__main__":
    unittest.main()
