import unittest

from evaluation.ragas_eval import evaluate_single


class RagasEvalSafetyTests(unittest.TestCase):
    def test_evaluate_single_returns_structured_status(self):
        result = evaluate_single(
            question="What is the policy?",
            contexts=["policy context"],
            answer="The policy is safety.",
            ground_truth="The policy is safety.",
        )

        self.assertIsInstance(result, dict)
        self.assertIn("status", result)
        self.assertIn(result["status"], {"ok", "skipped"})
        self.assertTrue(
            "result" in result or "error" in result,
            "expected either a scored result or a skip/error payload",
        )


if __name__ == "__main__":
    unittest.main()
