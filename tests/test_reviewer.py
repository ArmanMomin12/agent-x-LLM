
# test_reviewer.py
import unittest
from unittest.mock import patch, Mock
from temp_test_script import generate_plan, load_model  # import your functions

class TestReviewer(unittest.TestCase):

    @patch("temp_test_script.query_llm")
    def test_generate_plan_success(self, mock_query):
        # Arrange
        prompt = "Build an AI assistant"
        model = "llama3-70b-8192"
        mock_query.return_value = {"choices": [{"message": {"content": "Plan content"}}]}

        # Act
        import asyncio
        plan = asyncio.run(generate_plan(prompt, model))

        # Assert
        self.assertEqual(plan, "Plan content")

    @patch("temp_test_script.query_llm")
    def test_generate_plan_no_choices(self, mock_query):
        # Arrange
        prompt = "Some prompt"
        model = "llama3-70b-8192"
        mock_query.return_value = {}  # No 'choices' key

        # Act
        import asyncio
        plan = asyncio.run(generate_plan(prompt, model))

        # Assert
        self.assertIsNone(plan)

    @patch("temp_test_script.query_llm")
    def test_generate_plan_exception(self, mock_query):
        # Arrange
        prompt = "Some prompt"
        model = "llama3-70b-8192"
        mock_query.side_effect = Exception("Mocked exception")

        # Act
        import asyncio
        plan = asyncio.run(generate_plan(prompt, model))

        # Assert
        self.assertIsNone(plan)

    def test_load_model_success(self):
        # Arrange
        model_name = "llama3-70b-8192"

        # Act
        model = load_model(model_name)

        # Assert
        self.assertEqual(model, f"Loaded model {model_name}")

    def test_load_model_invalid(self):
        # Arrange
        model_name = "invalid-model"

        # Act & Assert
        with self.assertRaises(ValueError):
            load_model(model_name)

if __name__ == "__main__":
    unittest.main()


